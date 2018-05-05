#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
reload(sys)
sys.setdefaultencoding('euc-kr')
import codecs

class SVOExtractor(object):

    def load_dic(self):
        """ CSV 파일 로딩 , dictionary 형식(단어 - 분류)으로 저장 한 후 return"""
        reader = csv.reader(codecs.open('dic_file.csv', 'r', encoding='euc-kr'))
        entity = {}
        for row in reader:
            k, v = row
            entity[k] = v
        return entity

    def pos_tagging(self):
        """ 형태소 분석된 문장 return"""
#        s = "사람/NNG/이/JKS/차/NNG/와/JC/충돌/NNG/한다/XSV+EF"
#        s = "여자/NNG/남자/NNG/꼬마/NNG/애기/NNG/가/JKS/차/NNG/랑/JC/충돌/NNG/하/XSV"
#        s = "버스/NNG/가/JKS/건물/NNG/에/JC/충돌/NNG/했다/XSV"
#        s = "버스/NNG/가/JKS/자동차/NNG/와/JC/부/VV"
#        s = "트럭/NNG/이/JKS/건물/NNG/에/JC/충돌/NNG/했다/XSV" 
#        s = "오토바이/NNG/가/JKS/건물/NNG/에/JKB/충돌/NNG/했/XSV+EP/던/ETM/장면/NNG/입니다/VCP+EF"
#        s = "아이/NNG/가/JKS/전철/NNG/과/JC/충돌/NNG/했/XSV+EP/던/ETM/관경/NNG/입니다/VCP+EF/./SF"
#        s = "노인/NNG/이/JKS/버스/NNG/에/JKB/충돌/NNG/했/XSV+EP/던/ETM/상황/NNG/입니다/VCP+EF/./SF"
#        s = "오토바이/NNG/가/JKS/자동차/NNG/를/JKO/충동/NNG/하/XSV/는/ETM/상황/NNG/./SF"
#        s = "자동차/NNG/와/JC/자동차/NNG/가/JKS/맞부딪쳤/VV+EP/습니다/EF/./SF"
#        s = "택시/NNG/가/JKS/사물/NNG/에/JKB/충돌/NNG/했/XSV+EP/다/EF/./SF"
        s = "택시/NNG/가/JKS/난간/NNG/에/JKB/충돌/NNG/하/XSV/는/ETM/중/NNB/이/VCP/다/EC"
        s = s.decode('utf-8').encode('euc-kr')
        return s

    def svo_candidate_extraction(self, analyzed_str):
        """SVO 후보 단어 리스트 return"""
        candidate = analyzed_str.split('/')
    
        tmp = []
        sub_candidate =[]
        ob_candidate =[]
        v_candidate =[]
        
        count = 0
        while count < len(candidate):
            word = count
            word_class = count + 1

            tmp.append(candidate[count])

            if 'VV' in candidate[word_class]:
                v_candidate.append(candidate[word])  
            elif candidate[word_class] != 'NNG':
                tmp.remove(candidate[word])

            if candidate[word_class] == 'JKS':
                if len(tmp) == 1:
                     sub_candidate = tmp
                if len(tmp) > 1:
                    i = 0
                    tmp.reverse()
                    while i < len(tmp):
                        if i == 0 :
                            sub_candidate.append(tmp[0])
                        if i > 0 :
                            n = i
                            tmp_str = ""
                            while n >= 0 :
                                tmp_str += tmp[n]
                                n = n -1
                            sub_candidate.append(tmp_str)
                        i = i + 1 
                tmp = []         
            elif candidate[word_class] == 'JC' or candidate[word_class] == 'JKB' or candidate[word_class] == 'JKO' :
                if len(tmp) == 1:
                     ob_candidate = tmp
                if len(tmp) > 1:
                    i = 0
                    tmp.reverse()
                    while i < len(tmp):
                        if i == 0 :
                            ob_candidate.append(tmp[0])
                        if i > 0 :
                            n = i
                            tmp_str = ""
                            while n >= 0 :
                                tmp_str += tmp[n]
                                n = n -1
                            ob_candidate.append(tmp_str)
                        i = i + 1 
                tmp = []
            elif 'XSV' in candidate[word_class]:
                v_candidate = tmp
                tmp = []
            count = count + 2
        for j in sub_candidate:
            print(j)
        for s in ob_candidate:
            print(s)
        for g in v_candidate:
            print(g)    

        return sub_candidate ,ob_candidate ,v_candidate

    def svo_extraction(self,sub_candidate ,ob_candidate ,v_candidate, entity):
     
        final_ob = ""
        final_sub = ""
        final_v = ""

        """주어 찾기 """
        tmp = ""
        for x in list(sub_candidate):
            
            if x in entity:
                if len(tmp) < len(x) :
                    tmp = x
                    final_sub  = entity[x]          
        print("subject word candidate : "+ tmp)
        print("final subject : " + final_sub)
        if len(tmp) == 0:
            print("This word is not contained in dictionary")
 
        """ 목적어 찾기 """
        tmp = ""
        for x in list(ob_candidate):

            if x in entity:
                if len(tmp) < len(x) :
                    tmp = x
                    final_ob  = entity[x]
        print("object word candidate : " + tmp)      
        print("fianl object : "+ final_ob)
        if len(tmp) == 0:
            print("This word is not contained in dictionary")

        """ 동사 찾기"""
        key_str = " "
        key = entity.keys()
        for k in key:
            key_str += k + "/" 
        print("verd candidate : "+v_candidate[0])
      
        num = key_str.find(v_candidate[0])
        if num == -1:
            print("This word is not contained in dictionary : " + v_candidate[0] )
        else :
            tmp_key_str = key_str[num:]      
            num2 = tmp_key_str.find("/")
            final_v_str = tmp_key_str[:num2]
            final_v = entity[final_v_str]
            print("final word verd : " + final_v)

        return final_sub, final_ob, final_v

    def output_writer(self,word_class):
        print("S = " +word_class[0] + " O = " + word_class[1] + " V = " + word_class[2])
    

if __name__ == '__main__':
    S = SVOExtractor()
    entity = S.load_dic()
    analyzed_str = S.pos_tagging()
    SVO_candidate = S.svo_candidate_extraction(analyzed_str)
    word_class = S.svo_extraction(SVO_candidate[0] ,SVO_candidate[1] ,SVO_candidate[2], entity)
    S.output_writer(word_class)


      


