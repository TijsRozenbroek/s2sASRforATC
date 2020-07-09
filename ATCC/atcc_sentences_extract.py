# This script can be used to extract the separate utterances from the ATCC .trs
# files and write them to respective train, validation and test set
# .txt files. This thus makes .txt files with one utterance sentence
# per line, for all transcriptions.
# This can for example be used for making and testing a language model.
#
# It is written in a way that it can be called from a terminal
# (for compatibility across platforms). (tested and confirmed to work
# in a pycharm terminal in Windows 10 and a terminal in Ubuntu 18.04).
# It was built using python 3.7, so if it doesn't work,
# check whether you are using python 3.7 to run it.
#
# The way it can be executed in pycharm is by running the following
# in a terminal:
# `python atcc_sentences_extract.py --src [SOURCE] --dst [DESTINATION]`
# where SOURCE is the path to the directory of the dataset and
# DESTINATION is the path to where you want the .txt file to be written.
#
# In Ubuntu it can be executed with
# `python3.7 atcc_sentences_extract.py --src [SOURCE] --dst [DESTINATION]`

import os
import argparse
import sys
import re
import random
import numpy as np


__author__ = "Tijs Rozenbroek"

def replace_fix_homogenise(transcription):
    transcription = transcription.rstrip() + " "
    transcription = transcription.replace('[', ' [')
    transcription = transcription.replace(']', '] ')

    transcription = transcription.replace('[ground]', ' ')
    transcription = transcription.replace('[ground_|]', '')
    transcription = transcription.replace('[|_ground]', '')
    transcription = transcription.replace('[air]', ' ')
    transcription = transcription.replace('[air_|]', '')
    transcription = transcription.replace('[|_air]', '')
    transcription = transcription.replace('[unintelligible_|]', ' ')
    transcription = transcription.replace('[|_unintelligible]', '')
    transcription = transcription.replace('[noise_|]', '')
    transcription = transcription.replace('[|_noise]', '')
    transcription = transcription.replace('[speaker_|]', ' ')
    transcription = transcription.replace('[|_speaker]', ' ')
    transcription = transcription.replace('[|_background_speech]', '')
    transcription = transcription.replace('[background_speech_|]', '')

    # For czech and no_eng regular expression replacements further below
    transcription = transcription.replace('[unintelligible]', 'UNINT')
    transcription = transcription.replace('[noise]', 'NOISE')
    transcription = transcription.replace(' [ehm_??] ', ' EHM ')
    transcription = transcription.replace('[ehm_??]', ' EHM ')
    transcription = transcription.replace('[speaker]', 'SPEAKER')
    transcription = transcription.replace('[background_speech]', 'BACKGROUNDSPEECH')

    transcription = transcription.replace('(9(najn))', 'nine')
    transcription = transcription.replace('(9(njn))', 'nine')
    transcription = transcription.replace('(9 (najt))', 'nine')
    transcription = transcription.replace('(3(three))', 'three')
    transcription = transcription.replace(' ', '  ')
    transcription = transcription.replace(' 0 ', ' zero ')
    transcription = transcription.replace(' 1 ', ' one ')
    transcription = transcription.replace(' 2 ', ' two ')
    transcription = transcription.replace(' 3 ', ' tree ')
    transcription = transcription.replace(' 4 ', ' four ')
    transcription = transcription.replace(' 5 ', ' five ')
    transcription = transcription.replace(' 6 ', ' six ')
    transcription = transcription.replace(' 7 ', ' seven ')
    transcription = transcription.replace(' 8 ', ' eight ')
    transcription = transcription.replace(' 9 ', ' niner ')
    transcription = transcription.replace('0', ' zero ')
    transcription = transcription.replace('1', ' one ')
    transcription = transcription.replace('2', ' two ')
    transcription = transcription.replace('3', ' tree ')
    transcription = transcription.replace('4', ' four ')
    transcription = transcription.replace('5', ' five ')
    transcription = transcription.replace('6', ' six ')
    transcription = transcription.replace('7', ' seven ')
    transcription = transcription.replace('8', ' eight ')
    transcription = transcription.replace('9', ' niner ')

    transcription = transcription.replace('  ', ' ')

    # typos and errors
    transcription = transcription.replace('accelarating', 'accelerating')
    transcription = transcription.replace('accpet', 'accept')
    transcription = transcription.replace('actualy', 'actually')
    transcription = transcription.replace('Aerloft', 'aeroflot')
    transcription = transcription.replace('aeroswit', 'aerosvit')
    transcription = transcription.replace('Ausrtian', 'austrian')
    transcription = transcription.replace('afternon', 'afternoon')
    transcription = transcription.replace(' airborn ', ' airborne ')
    transcription = transcription.replace('allright', 'alright')
    transcription = transcription.replace('altitued', 'altitude')
    transcription = transcription.replace('apporach', 'approach')
    transcription = transcription.replace('appraoch', 'approach')
    transcription = transcription.replace('aproximately', 'approximately')
    transcription = transcription.replace('aproximetly', 'approximately')
    transcription = transcription.replace('availbale', 'available')
    transcription = transcription.replace('ARVEK', 'arveg')
    transcription = transcription.replace('untill', 'until')
    transcription = transcription.replace('Lufhansa', 'lufthansa')
    transcription = transcription.replace('Lufthasna', 'lufthansa')
    transcription = transcription.replace('Lufhtansa', 'lufthansa')
    transcription = transcription.replace('Luftahnsa', 'lufthansa')
    transcription = transcription.replace('Luftthansa', 'lufthansa')
    transcription = transcription.replace('bellow', 'below')
    transcription = transcription.replace('Beline', 'bee-transcription')
    transcription = transcription.replace('beeline', 'bee-transcription')
    transcription = transcription.replace('Bline', 'bee-transcription')
    transcription = transcription.replace('Beeeline', 'bee-transcription')
    transcription = transcription.replace('Blin', 'bee-transcription')
    transcription = transcription.replace('Beair', 'b_air')
    transcription = transcription.replace('Bair', 'b_air')
    transcription = transcription.replace('Buerou', 'b_air')
    transcription = transcription.replace('Bratair', 'britair')
    transcription = transcription.replace('Brusseles', 'brussels')
    transcription = transcription.replace('noice', 'noise')
    transcription = transcription.replace('fourty', 'forty')
    transcription = transcription.replace('Cimber', 'camber')
    transcription = transcription.replace('Charmwings', 'german wings')
    transcription = transcription.replace('coppied', 'copied')
    transcription = transcription.replace('comming', 'coming')
    transcription = transcription.replace('cotnact', 'contact')
    transcription = transcription.replace(' contac ', ' contact ')
    transcription = transcription.replace(' contac+ ', ' contact ')
    transcription = transcription.replace('conact', 'contact')
    transcription = transcription.replace('conatact', 'contact')
    transcription = transcription.replace('contace', 'contact')
    transcription = transcription.replace('Contactr', 'contract')
    transcription = transcription.replace(' Contrac ', ' contract ')
    transcription = transcription.replace('conntinue', 'continue')
    transcription = transcription.replace('cotinue', 'continue')
    transcription = transcription.replace(' Chech ', 'czech')
    transcription = transcription.replace('coorection', 'correction')
    transcription = transcription.replace('curcuit', 'circuit')
    transcription = transcription.replace('standart', 'standard')
    transcription = transcription.replace('aproved', 'approved')
    transcription = transcription.replace('controle', 'control')
    transcription = transcription.replace('clearence', 'clearance')
    transcription = transcription.replace('cleard', 'cleared')
    transcription = transcription.replace('clmbing', 'climbing')
    transcription = transcription.replace('deaparture', 'departure')
    transcription = transcription.replace('deaprture', 'departure')
    transcription = transcription.replace('degees', 'degrees')
    transcription = transcription.replace('degres', 'degrees')
    transcription = transcription.replace('dencending', 'descending')
    transcription = transcription.replace('decend', 'descend')
    transcription = transcription.replace('desend', 'descend')
    transcription = transcription.replace('desscend', 'descend')
    transcription = transcription.replace('Embrear', 'embraer')
    transcription = transcription.replace('Embreer', 'embraer')
    transcription = transcription.replace('establsih', 'establish')
    transcription = transcription.replace('estalbished', 'established')
    transcription = transcription.replace('etablished', 'established')
    transcription = transcription.replace(' EVENI ', ' evemi ')
    transcription = transcription.replace('extansion', 'extension')
    transcription = transcription.replace('Fineair', 'farner')
    transcription = transcription.replace('Finnari', 'finnair')
    transcription = transcription.replace('fomring', 'firming')
    transcription = transcription.replace('Gaule', 'gaulle')
    transcription = transcription.replace('gaule', 'gaulle')
    transcription = transcription.replace('Grosjet', 'grossjet')
    transcription = transcription.replace('groudn', 'ground')
    transcription = transcription.replace('headint', 'heading')
    transcription = transcription.replace('heding', 'heading')
    transcription = transcription.replace('hodling', 'holding')
    transcription = transcription.replace('hudred', 'hundred')
    transcription = transcription.replace('iformation', 'information')
    transcription = transcription.replace('inboud', 'inbound')
    transcription = transcription.replace('infomration', 'information')
    transcription = transcription.replace('interesction', 'intersection')
    transcription = transcription.replace('kntos', 'knots')
    transcription = transcription.replace('landa', 'land')
    transcription = transcription.replace('lenght', 'length')
    transcription = transcription.replace(' lengt ', ' length ')
    transcription = transcription.replace('Lod', 'lodz')
    transcription = transcription.replace('maintaing', 'maintaining')
    transcription = transcription.replace('maitain', 'maintain')
    transcription = transcription.replace('neagative', 'negative')
    transcription = transcription.replace('ninteen', 'nineteen')
    transcription = transcription.replace('ninty', 'ninety')
    transcription = transcription.replace(' Northshutt ', ' norshuttle ')
    transcription = transcription.replace(' Northshutt+ ', ' norshuttle ')
    transcription = transcription.replace('Northshuttel', 'norshuttle')
    transcription = transcription.replace('Northshuttle', 'norshuttle')
    transcription = transcription.replace('Northsthuttel', 'norshuttle')
    transcription = transcription.replace('Northsthuttle', 'norshuttle')
    transcription = transcription.replace('Nosrhutle', 'norshuttle')
    transcription = transcription.replace('occasionaly', 'occasionally')
    transcription = transcription.replace(' plese ', ' please ')
    transcription = transcription.replace('Polot', 'pollot')
    transcription = transcription.replace('possbile', 'possible')
    transcription = transcription.replace('Prhaa', 'praha')
    transcription = transcription.replace('procceding', 'proceeding')
    transcription = transcription.replace('pssing', 'passing')
    transcription = transcription.replace(' Qalit ', ' quality ')
    transcription = transcription.replace('Qality', 'quality')
    transcription = transcription.replace('qju', 'q_n_h')
    transcription = transcription.replace('recomend', 'recommend')
    transcription = transcription.replace('requsting', 'requesting')
    transcription = transcription.replace('restrctions', 'restrictions')
    transcription = transcription.replace('restrisction', 'restriction')
    transcription = transcription.replace('Ruyzn', 'ruzyne')
    transcription = transcription.replace(' Ruzyn ', ' ruzyne ')
    transcription = transcription.replace('shotrcut', 'shortcut')
    transcription = transcription.replace('Skyravel', 'skytravel')
    transcription = transcription.replace('Skytavel', 'skytravel')
    transcription = transcription.replace('Skytrevel', 'skytravel')
    transcription = transcription.replace(' Smartwing ', ' smartwings ')
    transcription = transcription.replace('squwak', 'squawk')
    transcription = transcription.replace('sss', 's')
    transcription = transcription.replace('suffician', 'sufficient')
    transcription = transcription.replace(' thats ', " that's ")
    transcription = transcription.replace('therell', "there'll")
    transcription = transcription.replace('thosuand', 'thousand')
    transcription = transcription.replace('thouasand', 'thousand')
    transcription = transcription.replace('Timeair', 'time air')
    transcription = transcription.replace('timecheck', 'time check')
    transcription = transcription.replace('trafic', 'traffic')
    transcription = transcription.replace(' +uftahnsa ', ' lufthansa ')
    transcription = transcription.replace(' +uzyn ', ' ruzyne ')
    transcription = transcription.replace(' vacat ', ' vacate ')
    transcription = transcription.replace('Vlaim', 'vlasim')
    transcription = transcription.replace(' Voi+ ', ' vozytse ')
    transcription = transcription.replace('wchich', 'which')
    transcription = transcription.replace('Windgoose', 'twingoose')
    transcription = transcription.replace('Wingoose', 'twingoose')
    transcription = transcription.replace('Wizair', 'wizzair')
    transcription = transcription.replace('Wizziar', 'wizzair')
    transcription = transcription.replace('Wunair', 'southern air')
    transcription = transcription.replace('Yangzte', 'yangtze')

    transcription = transcription.replace('appron', 'UNINT')
    transcription = transcription.replace('Ladyrasim', 'UNINT')

    transcription = transcription.replace('(Contract (kontrakt))', 'contract')
    transcription = transcription.replace('(turn(trn))', 'turn')
    transcription = transcription.replace('(turn(t?r))', 'turn')
    transcription = transcription.replace('(QNH(kjenej?))', 'q_n_h')
    transcription = transcription.replace('(QNH(kjenej))', 'q_n_h')
    transcription = transcription.replace('(QNH(kj?enej?))', 'q_n_h')
    transcription = transcription.replace('(QNH(kj?enejd?))', 'q_n_h')
    transcription = transcription.replace('(ILS(jeles))', 'i_l_s')
    transcription = transcription.replace('(CSA(svis))', 'c_s_a')
    transcription = transcription.replace('(CSA (s es))', 'c_s_a')
    transcription = transcription.replace('(CS+ (s es))', 'c_s_a')
    transcription = transcription.replace('( +SA (es ej))', 'c_s_a')
    transcription = transcription.replace('(C+ (s))', 'c_s_a')
    transcription = transcription.replace('( +SA (sej))', 'c_s_a')
    transcription = transcription.replace('(TCAS(týkas))', 't_c_a_s')
    transcription = transcription.replace('(TCAS (tkas))', 't_c_a_s')
    transcription = transcription.replace('(TMA(t em ej))', 't_m_a')
    transcription = transcription.replace('(TMA (t em ej))', 't_m_a')
    transcription = transcription.replace('(TMA (t em aj))', 't_m_a')
    transcription = transcription.replace('(TMA(temej))', 't_m_a')
    transcription = transcription.replace('FL', 'flight level')
    transcription = transcription.replace('(turn(térn))', 'turn')
    transcription = transcription.replace('(H(otel))', 'hotel')
    transcription = transcription.replace('(heading(eding))', 'heading')
    transcription = transcription.replace('(heading (hidink))', 'heading')
    transcription = transcription.replace('(IFR(jefr))', 'i_f_r')
    transcription = transcription.replace('(IFR(jef))', 'i_f_r')
    transcription = transcription.replace('(VFR(vefr))', 'v_f_r')
    transcription = transcription.replace('(ATC (ej t s))', 'a_t_c')
    transcription = transcription.replace('(ATC(ej t s))', 'a_t_c')
    transcription = transcription.replace('(US (j? es))', 'u_s')
    transcription = transcription.replace('(EFC( ef s))', 'e_f_c')
    transcription = transcription.replace('(ATR (ej t r))', 'a_t_r')
    transcription = transcription.replace('(CTO (s t ou))', 'c_t_o')
    transcription = transcription.replace('(VOR (vjor))', 'v_o_r')
    transcription = transcription.replace('(CRJ (s r dej))', 'c_r_j')
    transcription = transcription.replace('(DME (d em ))', 'd_m_e')
    transcription = transcription.replace('(FIR (ef j r))', 'f_i_r')
    transcription = transcription.replace('(VMC(v em s))', 'v_m_c')
    transcription = transcription.replace('(ATR (ej t r))', 'a_t_r')

    transcription = transcription.replace(' ILS ', ' i_l_s ')
    transcription = transcription.replace(' IFR ', ' i_f_r ')
    transcription = transcription.replace('TCAS', 't_c_a_s')
    transcription = transcription.replace('CSA', 'c_s_a')
    transcription = transcription.replace(' QNH ', ' q_n_h ')
    transcription = transcription.replace(' ATC ', ' a_t_c ')
    transcription = transcription.replace(' RWY ', ' runway ')
    transcription = transcription.replace(' VLM ', ' vlasim ')
    transcription = transcription.replace(' VOZ ', ' vozytse ')
    transcription = transcription.replace(' HDO ', ' hermsdorf ')
    transcription = transcription.replace('(LLZ(localizer))', 'localizer')
    transcription = transcription.replace(' LLZ ', ' localizer ')

    transcription = transcription.replace('( zero (ou))', 'o')
    transcription = transcription.replace('( zero  (ou))', 'o')
    transcription = transcription.replace('(radar(rejdr))', 'radar')
    transcription = transcription.replace('(radar (rejda))', 'radar')
    transcription = transcription.replace('(radar(rejda))', 'radar')
    transcription = transcription.replace('(radar (rdar))', 'radar')
    transcription = transcription.replace('(radar(rdar))', 'radar')
    transcription = transcription.replace('(radar(rrradar))', 'radar')
    transcription = transcription.replace('(radar(radar))', 'radar')
    transcription = transcription.replace('(radar (radar))', 'radar')
    transcription = transcription.replace('(tower(tavr))', 'tower')
    transcription = transcription.replace('(sequence(sekvenc))', 'sequence')
    transcription = transcription.replace('(yes (ja))', 'ja')
    transcription = transcription.replace('(yes (j))', 'ja')
    transcription = transcription.replace('(yes (je))', 'yes')
    transcription = transcription.replace('(yes (jea))', 'yeah')
    transcription = transcription.replace('(through (dr))', 'through')
    transcription = transcription.replace('(through (dr?))', 'through')
    transcription = transcription.replace('(own (avn))', 'own')
    transcription = transcription.replace('(and (a))', 'and')
    transcription = transcription.replace('(a (ej))', 'a')
    transcription = transcription.replace('(a(ej))', 'a')
    transcription = transcription.replace('(A(ej))', 'a')
    transcription = transcription.replace('(a ())', 'ah')
    transcription = transcription.replace('(C(si))', 'c')
    transcription = transcription.replace('(F(foks))', 'fox')
    transcription = transcription.replace('(F(fox))', 'fox')
    transcription = transcription.replace('(X (iks))', 'x')
    transcription = transcription.replace('(X(iks))', 'x')
    transcription = transcription.replace('(X(eks))', 'x')
    transcription = transcription.replace('(V (v))', 'v')
    transcription = transcription.replace('(V(v))', 'v')
    transcription = transcription.replace('(V(vee))', 'v')
    transcription = transcription.replace('(R (r))', 'r')
    transcription = transcription.replace('(R(r))', 'r')
    transcription = transcription.replace('(R(ar))', 'r')
    transcription = transcription.replace('( two  (tr))', 'true')
    transcription = transcription.replace('(again(egan))', 'again')
    transcription = transcription.replace('(approach (eproui))', 'approach')
    transcription = transcription.replace('(approachi (aproui))', 'approach')
    transcription = transcription.replace('(Mun+ (min))', 'mun')
    transcription = transcription.replace('good bye', 'goodbye')

    transcription = transcription.replace('(Czech Air Force(?ajkefors))', 'czech air force')
    transcription = transcription.replace('(French Navy (fren? nejvy))', 'french navy')
    transcription = transcription.replace('(Swede Star (svd str))', 'swede star')
    transcription = transcription.replace('(Air Berlin(Berlin))', 'berlin')
    transcription = transcription.replace('(Grossjet (grosdet))', 'grossjet')
    transcription = transcription.replace('(Thomson (tomson))', 'tomson')
    transcription = transcription.replace('(Majestic (mad?estyk))', 'majestic')
    transcription = transcription.replace('(Ascot (askot))', 'ascot')
    transcription = transcription.replace('(Air China (er?ajna))', 'air china')
    transcription = transcription.replace('(Vinair (vinr))', 'vinair')
    transcription = transcription.replace('(Silver Arrows (silvr erous))', 'silver arrows')
    transcription = transcription.replace('(Germania (germnija))', 'germania')
    transcription = transcription.replace('(American (mericken))', 'american')
    transcription = transcription.replace('(Dynasty (dajnasty))', 'dynasty')
    transcription = transcription.replace('(Navigator (navigejtr))', 'navigator')
    transcription = transcription.replace('(Martinair (martinr))', 'martinair')
    transcription = transcription.replace('(Etiopian (ejtyjopen))', 'ethiopian')
    transcription = transcription.replace('(Midland (midlend))', 'midland')
    transcription = transcription.replace('(Black Sea (blek s))', 'black sea')
    transcription = transcription.replace('(Gulf Air (galf r))', 'gulf air')
    transcription = transcription.replace('(Siberia (siberyja))', 'siberia')
    transcription = transcription.replace('(Kingfisher (kingfi?r))', 'kingfisher')
    transcription = transcription.replace('(Tujet (tdet))', 'tujet')
    transcription = transcription.replace('(El Al (elal))', 'el al')
    transcription = transcription.replace('(Airbridge Cargo (rbrid kargo))', 'airbridge cargo')
    transcription = transcription.replace('(Cargolux (kargolux))', 'cargolux')
    transcription = transcription.replace('(Croatian (krocije))', 'croatian')
    transcription = transcription.replace('(Charter Ukraine (?rtr ukrajin))', 'charter ukraine')
    transcription = transcription.replace('(Binair (binr))', 'binair')
    transcription = transcription.replace('(Bluefin (blfin))', 'bluefin')
    transcription = transcription.replace('(Russia (rasija))', 'russia')
    transcription = transcription.replace('(Fly Niki (flaj nyky))', 'fly niki')
    transcription = transcription.replace('(UPS (j? p es))', 'u_p_s')
    transcription = transcription.replace('KLM', 'k_l_m')

    transcription = transcription.replace('(PISAM (PIZEM))', 'pisam')
    transcription = transcription.replace('(OMELO (emelo))', 'omelo')
    transcription = transcription.replace(' (APRON (ejpron)) ', ' apron ')
    transcription = transcription.replace('(Warsaw (Var?ava))', 'warsaw')
    transcription = transcription.replace('(Warsaw(Var?ava))', 'warsaw')
    transcription = transcription.replace('(Warsaw(Var?ava))', 'warsaw')
    transcription = transcription.replace('(Warsaw (varsava))', 'warsaw')
    transcription = transcription.replace('(Warsaw(var?ava))', 'warsaw')
    transcription = transcription.replace('(Warsaw (varava))', 'warsaw')
    transcription = transcription.replace('(Warsaw (var?ava))', 'warsaw')
    transcription = transcription.replace('(Warsaw (Varsava))', 'warsaw')
    transcription = transcription.replace('(Warsaw (Var?ava))', 'warsaw')
    transcription = transcription.replace('(Munich (minn))', 'munich')
    transcription = transcription.replace('(Munich (minchn))', 'munich')
    transcription = transcription.replace('(Munich(minchen))', 'munich')
    transcription = transcription.replace('(Munchen (mien))', 'munich')
    transcription = transcription.replace('(Munich(mynchen))', 'munich')
    transcription = transcription.replace('(Munich (minchen))', 'munich')
    transcription = transcription.replace('(Munchen (minchn))', 'munich')
    transcription = transcription.replace('(Munchen (mi?en))', 'munich')
    transcription = transcription.replace('(Munchen (min?n))', 'munich')
    transcription = transcription.replace('(Munchen (min?en))', 'munich')
    transcription = transcription.replace('(Munich(mynchn))', 'munich')
    transcription = transcription.replace('(Munich(mjunyk))', 'munich')
    transcription = transcription.replace('(Munchen (mi?n))', 'munich')
    transcription = transcription.replace('(Munchen ( min?n))', 'munich')
    transcription = transcription.replace('(Munich(mi?n))', 'munich')
    transcription = transcription.replace('(Munich (min?en))', 'munich')
    transcription = transcription.replace('(Munich (min?n))', 'munich')
    transcription = transcription.replace('(Praha(Prague))', 'prague')
    transcription = transcription.replace('(Praha (praga))', 'praha')
    transcription = transcription.replace('(Praha (pracha))', 'praha')
    transcription = transcription.replace('(Praha(prg))', 'prague')
    transcription = transcription.replace('(Praha(Prg))', 'prague')
    transcription = transcription.replace('(Praha(Praga))', 'praga')
    transcription = transcription.replace('(Praha(praga))', 'praga')
    transcription = transcription.replace('(Praha (Praga))', 'praga')
    transcription = transcription.replace('(Praha(prag))', 'prague')
    transcription = transcription.replace('(Praha(Prag))', 'prague')
    transcription = transcription.replace('(Cheb (?eb))', 'cheb')
    transcription = transcription.replace('(Cheb (eb))', 'cheb')
    transcription = transcription.replace('(Cheb (cheb))', 'cheb')
    transcription = transcription.replace('(Vlaim (vilasimim))', 'vlasim')
    transcription = transcription.replace('(vlasim (vilasimim))', 'vlasim')
    transcription = transcription.replace('(Ruzyn(ruzn))', 'ruzyne')
    transcription = transcription.replace('(Ruzyn?(ruzn))', 'ruzyne')
    transcription = transcription.replace('(Ruzyn(ruzyn))', 'ruzyn')
    transcription = transcription.replace('(Ruzyn?(ruzyn))', 'ruzyn')
    transcription = transcription.replace('(Vienna(vn))', 'vienna')
    transcription = transcription.replace('(Wien (vijena))', 'vienna')
    transcription = transcription.replace('(Vienna (vijena))', 'vienna')
    transcription = transcription.replace('(Rhein(rajn))', 'rhein')
    transcription = transcription.replace('(Rhein (rajn))', 'rhein')
    transcription = transcription.replace('(Hamburg(Hambruk))', 'hamburg')
    transcription = transcription.replace('(Hamburg(hambruk))', 'hamburg')
    transcription = transcription.replace('(Hole?ov(holesov))', 'holesov')
    transcription = transcription.replace('Pbram', 'Pribram')

    transcription = transcription.replace(' ', '  ')

    transcription = transcription.replace(' A ', ' alfa ')
    transcription = transcription.replace(' B ', ' bravo ')
    transcription = transcription.replace(' C ', ' charlie ')
    transcription = transcription.replace(' D ', ' delta ')
    transcription = transcription.replace(' E ', ' echo ')
    transcription = transcription.replace(' F ', ' foxtrot ')
    transcription = transcription.replace(' G ', ' golf ')
    transcription = transcription.replace(' H ', ' hotel ')
    transcription = transcription.replace(' I ', ' india ')
    transcription = transcription.replace(' J ', ' juliett ')
    transcription = transcription.replace(' K ', ' kilo ')
    transcription = transcription.replace(' L ', ' lima ')
    transcription = transcription.replace(' M ', ' mike ')
    transcription = transcription.replace(' N ', ' november ')
    transcription = transcription.replace(' O ', ' oscar ')
    transcription = transcription.replace(' P ', ' papa ')
    transcription = transcription.replace(' Q ', ' quebec ')
    transcription = transcription.replace(' R ', ' romeo ')
    transcription = transcription.replace(' S ', ' sierra ')
    transcription = transcription.replace(' T ', ' tango ')
    transcription = transcription.replace(' U ', ' uniform ')
    transcription = transcription.replace(' V ', ' victor ')
    transcription = transcription.replace(' W ', ' whiskey ')
    transcription = transcription.replace(' X ', ' x_ray ')
    transcription = transcription.replace(' Y ', ' yankee ')
    transcription = transcription.replace(' Z ', ' zulu ')

    transcription = transcription.replace('  ', ' ')
    transcription = transcription.replace('  ', ' ')
    transcription = transcription.replace('  ', ' ')

    transcription = transcription.replace('+', '')
    transcription = transcription.replace('.', '')
    transcription = transcription.replace('??', '%')
    transcription = transcription.replace('?', '')
    transcription = transcription.replace('%', '??')

    transcription = transcription.lower()

    transcription = re.sub(
        "\[czech\_\|\]([\w*\s*\?*\(*\)*]*)[^\[czech\_\|\]]([\w*\s*\?*\(*\)*]*)\[\|\_czech\]",
        "E",
        transcription)
    transcription = re.sub(
        "\[no\_eng\_\|\]([\w*\s*\?*\(*\)*]*)[^\[no\_eng\_\|\]]([\w*\s*\?*\(*\)*]*)\[\|\_no\_eng\]",
        "E", transcription)

    transcription = transcription.replace('_', ' ')

    transcription = transcription.replace('noise', 'N')
    transcription = transcription.replace('unint', 'U')
    transcription = transcription.replace('speaker', 'S')
    transcription = transcription.replace('backgroundspeech', 'B')
    transcription = transcription.replace(' ehm ', ' H ')

    # homogeneity and correction
    transcription = transcription.replace('air berlin', 'air_berlin')
    transcription = transcription.replace('air bridge', 'airbridge')
    transcription = transcription.replace('airbridge cargo', 'airbridge_cargo')
    transcription = transcription.replace('air france', 'airfrans')
    transcription = transcription.replace('airfrance', 'airfrans')
    transcription = transcription.replace('bee transcription', 'bee-transcription')
    transcription = transcription.replace('beeline', 'bee-transcription')
    transcription = transcription.replace('black sea', 'black_sea')
    transcription = transcription.replace('blacksea', 'black_sea')
    transcription = transcription.replace('charles de gaulle', 'charles_de_gaulle')
    transcription = transcription.replace('de gaulle', 'de_gaulle')
    transcription = transcription.replace('çharter ukraine', 'charter_ukraine')
    transcription = transcription.replace('czech air force', 'czech_air_force')
    transcription = transcription.replace('czech force', 'czech_force')
    transcription = transcription.replace('french navy', 'french_navy')
    transcription = transcription.replace('german cargo', 'german_cargo')
    transcription = transcription.replace('germanwings', 'german_wings')
    transcription = transcription.replace('german wings', 'german_wings')
    transcription = transcription.replace('gulf air', 'gulf_air')
    transcription = transcription.replace('jet airways', 'jet_airways')
    transcription = transcription.replace('lady racine', 'lady_racine')
    transcription = transcription.replace('norshuttle', 'nor_shuttle')
    transcription = transcription.replace('oman air', 'oman_air')
    transcription = transcription.replace('silver arrows', 'silver_arrows')
    transcription = transcription.replace('smart lynx', 'smart_lynx')
    transcription = transcription.replace('southernair', 'southern_air')
    transcription = transcription.replace('southern air', 'southern_air')
    transcription = transcription.replace('tel aviv', 'tel_aviv')
    transcription = transcription.replace('time air', 'time_air')
    transcription = transcription.replace('twinstar', 'twin_star')
    transcription = transcription.replace('twin star', 'twin_star')
    transcription = transcription.replace('ukraine charter', 'ukraine_charter')
    transcription = transcription.replace('ukraine international', 'ukraine_international')
    transcription = transcription.lstrip()

    return transcription

def shuffle_and_write(transcriptions):
    random.Random(15400031944529420895).shuffle(transcriptions)
    train_val_test = np.split(transcriptions, [int(.8 * len(transcriptions)), int(.9 * len(transcriptions))])
    arrays = ["atcctrainlines", "atccvalidlines", "atcctestlines"]
    for i in range(3):
        dst_file_name = arrays[i] + ".txt"
        dst = os.path.join(args.dst, dst_file_name)
        with open(dst, "w", encoding='utf-8', errors='ignore') as dst_file:
            for transcription in train_val_test[i]:
                separate_lines = transcription.split('@')  # Using the custom introduced character to split based on lines
                for sep_line in separate_lines:
                    sep_line = sep_line.rstrip()
                    sep_line = sep_line.lstrip()
                    if sep_line != '' and sep_line != ' ':
                        dst_file.write(f"{sep_line}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ATCC-train line extraction.")
    parser.add_argument("--src", help="Data source directory")
    parser.add_argument("--dst", help=".txt file destination directory")
    args = parser.parse_args()

    assert os.path.isdir(str(args.src)), "Data source directory not found"
    os.makedirs(args.dst, exist_ok=True)

    sys.stdout.write("Processing...\n")
    sys.stdout.flush()

    transcriptions = []
    counter = 0
    for file in os.listdir(args.src):
        if file.endswith(".trs"):
            trs_file_path = os.path.join(args.src, file)

            with open(trs_file_path, encoding='utf-8', errors='ignore') as file_xml:
                transcription = ""
                for trs_line in file_xml.readlines():
                    if not trs_line.startswith('<') and not trs_line.startswith('..'):
                        counter+=1
                        transcription += trs_line.rstrip() + " @ "

                transcription = replace_fix_homogenise(transcription)
                transcriptions.append(transcription)

    shuffle_and_write(transcriptions)


