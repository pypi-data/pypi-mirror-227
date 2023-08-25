#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (C) 2020  David Arroyo Menéndez (davidam@gmail.com)
# This file is part of Damegender.

# Author: David Arroyo Menéndez <davidam@gmail.com>
# Maintainer: David Arroyo Menéndez <davidam@gmail.com>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with DameGender; see the file GPL.txt.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,


import requests
import json
import os
from app.dame_gender import Gender
from app.dame_utils import DameUtils
du = DameUtils()


class DameGenderApi(Gender):

    def get(self, name):
        # it allows to download a name from an API
        if (self.config['DEFAULT']['genderapi'] == 'yes'):
            fichero = open("files/apikeys/genderapipass.txt", "r+")
            contenido = fichero.readline()
            contenido = contenido.replace('\n', '')
            string = 'https://gender-api.com/get?name=' + name
            string = string + '&key=' + contenido
            r = requests.get(string)
            j = json.loads(r.text)
            v = [j['gender'], j['accuracy'], j['samples']]
        return v

    def guess(self, name, gender_encoded=False):
        # returns a gender from a name
        v = self.get(name)
        if (self.config['DEFAULT']['genderapi'] == 'yes'):
            guess = v[0]
            if (guess == 'male'):
                if gender_encoded:
                    guess = 1
            elif (guess == 'female'):
                if gender_encoded:
                    guess = 0
            else:
                if gender_encoded:
                    guess = 2
                else:
                    guess = 'unknown'
        else:
            if gender_encoded:
                guess = 2
            else:
                guess = 'unknown'
        return guess

    def accuracy(self, name):
        # returns the percentage of men or women using a name
        v = self.get(name)
        return v[1]

    def samples(self, name):
        # returns the number of people using a name
        v = self.get(name)
        return v[2]

    def download(self, path="files/names/partial.csv", *args, **kwargs):
        # download a json of people's names from a csv given
        name_position = kwargs.get('name_position', 0)
        genderapipath = "files/names/genderapi" + du.path2file(path) + ".json"
        backup = kwargs.get('backup', genderapipath)
        fichero = open("files/apikeys/genderapipass.txt", "r+")
        if backup:
            backup = open(backup, "w+")
        else:
            backup = open(genderapipath, "w+")
        contenido = fichero.readline()
        contenido = contenido.replace('\n', '')
        string = ""
        names = self.csv2names(path, name_position=name_position)
        names_list = du.split(names, 20)
        jsondict = {'names': []}
        string = ""
        for l1 in names_list:
            # generating names string to include in url
            count = 1
            stringaux = ""
            for n in l1:
                if (len(l1) > count):
                    stringaux = stringaux + n + ";"
                else:
                    stringaux = stringaux + n
                count = count + 1
            url1 = 'https://gender-api.com/get?name=' + stringaux
            url1 = url1 + '&multi=true&key=' + contenido
            r = requests.get(url1)
            j = json.loads(r.text)
            jsondict['names'].append(j['result'])
        jsonv = json.dumps(jsondict)
        backup.write(jsonv)
        backup.close()
        return 1

    def download_csv(self, path="files/names/partial.csv", *args, **kwargs):
        # download a csv of people's names from a csv given
        dir0 = 'files/tmp/'
        if (not os.path.exists(dir0)):
            os.mkdir('files/tmp/')
        backup_all = kwargs.get('backup_all',
                                dir0 + 'genderapiall.csv')
        backup_females = kwargs.get('backup_females',
                                    dir0 + 'genderapifemales.csv')
        backup_males = kwargs.get('backup_males',
                                  dir0 + 'genderapimales.csv')
        name_position = kwargs.get('name_position', 0)
        names = self.csv2names(path, name_position=name_position)
        if backup_females:
            file_females = open(backup_females, "w+")
        if backup_males:
            file_males = open(backup_males, "w+")
        if backup_all:
            file_all = open(backup_all, "w+")

        for i in names:
            name = self.get(i)
            guess = self.guess(i)
            if (guess == "female"):
                file_females.write(str(i)+","+str(name[2])+"\n")
            if (guess == "male"):
                file_males.write(str(i)+","+str(name[2])+"\n")
            if ((guess == "male") or (guess == "female")):
                file_all.write(str(i)+","+str(name[2])+"\n")
        file_females.close()
        file_males.close()
        file_all.close()
        return 1

    def json2gender_list(self, jsonf="", gender_encoded=False):
        # transforms the json into a gender_encoded array of males and females
        jsondata = open(jsonf).read()
        json_object = json.loads(jsondata)
        guesslist = []
        for i in json_object["names"][0]:
            if gender_encoded:
                if (i["gender"] == 'female'):
                    guesslist.append(0)
                elif (i["gender"] == 'male'):
                    guesslist.append(1)
                else:
                    guesslist.append(2)
            else:
                guesslist.append(i["gender"])
        return guesslist

    def json2names(self, jsonf="", surnames=False):
        # transforms the json into an array of male and female names
        jsondata = open(jsonf).read()
        json_object = json.loads(jsondata)
        nameslist = []
        for i in json_object["names"][0]:
            if (i["name"] != ''):
                if surnames:
                    nameslist.append([i["name"], i["surname"]])
                else:
                    nameslist.append(i["name"])
        return nameslist

    def guess_list(self, path="files/names/partial.csv", gender_encoded=False):
        # returns a list of males, females
        fichero = open("files/apikeys/genderapipass.txt", "r+")
        contenido = fichero.readline()
        string = ""
        names = self.csv2names(path)
        list_total = []
        names_list = du.split(names, 20)
        for l1 in names_list:
            count = 1
            string = ""
            for n in l1:
                if (len(l1) > count):
                    string = string + n + ";"
                else:
                    string = string + n
                count = count + 1
            url = 'https://gender-api.com/get?name='
            url = url + string + '&multi=true&key=' + contenido
            r = requests.get(url)
            d = json.loads(r.text)
            slist = []
            for item in d['result']:
                if (((item['gender'] is None) or
                     (item['gender'] == 'unknown')) & gender_encoded):
                    slist.append(2)
                elif (((item['gender'] is None) or
                       (item['gender'] == 'unknown')) & (not gender_encoded)):
                    slist.append("unknown")
                elif ((item['gender'] == "male") & gender_encoded):
                    slist.append(1)
                elif ((item['gender'] == "male") & (not gender_encoded)):
                    slist.append("male")
                elif ((item['gender'] == "female") & gender_encoded):
                    slist.append(0)
                elif ((item['gender'] == "female") & (not gender_encoded)):
                    slist.append("female")
            # print("string: " + string)
            # print("slist: " + str(slist))
            # print("slist len:" + str(len(slist)))
            list_total = list_total + slist
        return list_total

    def apikey_limit_exceeded_p(self):
        # returns a boolean explaining if the limit
        # has been exceeded
        j = ""
        limit_exceeded_p = True
        if (self.config['DEFAULT']['genderapi'] == 'yes'):
            fichero = open("files/apikeys/genderapipass.txt", "r+")
            contenido = fichero.readline()
            contenido = contenido.replace('\n', '')
            string = 'https://gender-api.com/get-stats?key=' + contenido
            r = requests.get(string)
            j = json.loads(r.text)
            limit_exceeded_p = j["is_limit_reached"]
        return limit_exceeded_p

    def apikey_count_requests(self):
        # returns the count of request done to the API
        count = -1
        if (self.config['DEFAULT']['genderapi'] == 'yes'):
            fichero = open("files/apikeys/genderapipass.txt", "r+")
            contenido = fichero.readline()
            contenido = contenido.replace('\n', '')
            string = 'https://gender-api.com/get-stats?key=' + contenido
            r = requests.get(string)
            j = json.loads(r.text)
            count = j["remaining_requests"]
        return count
