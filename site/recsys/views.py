# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    return render(request, 'rec/recsys.html', {})


def recommendations(request):
    return JsonResponse({
        "abstract": "Wireless meshnet8Ex8 (WMNs)consist of meshrout6L and meshclient8 where meshroutfix have minimal mobilit  and formtr backbone of WMNs. They provide netide access for bot mesh andconvent1)fi8 clientt TheintL gratLfl of WMNs wit ot8 net8866 such as t1Int6fiPx1 cellular, IEEE 802.11, IEEE 802.15, IEEE 802.16, sensor netsor1L ets can be accomplishedtccomp tc gatomp and bridging functng1 in t1 meshroutfijx Meshclient can be eit8fi st8fij1)6x or mobile, and can form aclient meshnet16S amongtng1fifiELj and wit meshroutLfifi WMNs are antLfifl1)6fl t resolvets limit18fiflfl andt significantfl improvetp performance of ad hocnetLEP8L wireless local area net1Pxx (WLANs), wireless personal areanet16fij (WPANs), and wirelessmetess1fifljfl areanet1LPS (WMANs). They are undergoing rapid progress and inspiring numerousdeploymentS WMNs will deliver wireless services for a largevariet ofapplicat6fifl in personal, local, campus, andmet8Lfix1)6fi areas. Despit recent advances in wireless mesh netjLfiP1)6 many research challenges remain in allprotjfiS layers. This paperpresent adetEfl81 stEonrecent advances and open research issues in WMNs. Syst1 architL881)6 andapplicat)68 of WMNs are described, followed by discussingts critssi factss influencingprotenc design.Theoret8fiL netore capacit and tdst1LLSjx tt1LL protLLSj for WMNs are exploredwit anobjectE1 t point out a number of open research issues. Finally,tnal beds,indust681 pract68 andcurrent strent actntx1) relatt t WMNs arehighlight8x  # 2004 Elsevier B.V. Allrl rl  KedI7-8 Wireless meshnet186flfl Ad hocnet8jEES Wireless sensornetor16fl Medium accessconts1fi Routs1 prots1fiS Transport protspor ScalabilitS Securiti Powermanagement andcontfi8fl Timingsynchronizat ion 1389-1286/$ - seefront matt # 2004 Elsevier B.V. Allright reserved. doi:10....",
        "author": [
            "Ian F. Akyildiz",
            "Xudong Wang 0001",
            "Weilin Wang"
        ],
        "citation_contexts": [
            ", and other factors, the change may be frequent and may cause large variations in RTT. This will degrade the TCP performance, because the normal operation of TCP relies on a smooth measurement of RTT =-=[1]-=-. How to enhance a TCP so that it is robust to large RTT variations has not been thoroughly studied for both mobile ad hoc networks and WMNs. 10.1.2. Entirely new transport protocols As discussed befo",
            "within the global network is difficult to achieve [62]. Thus, distributed multiple access schemes such as CSMA/ CA are more favorable. However, CSMA/CA has very low frequency spatial-reuse efficiency =-=[2]-=-, which significantly limits the scalability of CSMA/CA-based multi-hop networks. To improve the scalability of WMNs, designing a hybrid multiple access scheme with CSMA/CA and TDMA or CDMA is an inte ped for the purpose of reducing power consumptions [33,147,131]. These schemes reduce exposed nodes problem, especially in a dense network, and thus, improve the spectrum spatial-reuse factor in WMNs =-=[2]-=-. However, hidden nodes still exist and may become worse because lower transmission power level reduces the possibility of detecting a potential interfering node [72]. \u2022 Proposing innovative MAC proto",
            "ks 47 (2005) 445\u2013487 455 capacity and flexibility of wireless systems. Typical examples include directional and smart antennas [117,124], MIMO systems [139,126], and multi-radio/multi-channel systems =-=[122,3]-=-. To date, MIMO has become one of the key technologies for IEEE 802.11n [64], the high speed extension of Wi-Fi. Multi-radio chipsets and their development platforms are available on the market [44].  ach radio contains both MAC and physical layers, in order to make a multi-radio network work as a single node, a virtual MAC protocol is usually required to coordinate the communication in all radios =-=[3]-=-. For a wireless network, the frequency band is a very precious resource. However, many of existing allocated frequency bands (both licensed and unlicensed) have not been utilized efficiently. Measure  has multiple radios each with its own MAC and physical layers. Communications in these radios are totally independent. Thus, a virtual MAC protocol such as the multi-radio unification protocol (MUP) =-=[3]-=- is required on top of MAC to coordinate communications in all channels. In fact one radio can have multiple channels. However, for simplicity of design and application, a single channel is used in ea number of hops and nodes. \u2022 The channel switching time may be much larger than 224 ls [122]. A larger channel switching time will significantly degrade the performance of a multi-channel MAC protocol =-=[3]-=-. \u2022 Channel selection criterion based on the lowest number of source\u2013destination pairs for each I.F. Akyildiz et al. / Computer Networks 47 (2005) 445\u2013487 463 channel is not always appropriate. Using  IM/ATIMACK (for default channel) procedures. In MUP, there are multiple wireless network interface cards (NICs) on each node. Channels on all NICs are orthogonal and fixed. The major functions of MUP =-=[3]-=- include: \u2022 Discovering neighbors. After the discovering procedures, neighbors are classified into MUPenabled and legacy nodes. \u2022 Selecting a NIC based on one-hop round trip time (RTT) measurements. M"
        ],
        "cited_paper_doi": [
            "1885924",
            "3716989",
            "378304",
            "297741",
            "3716990",
            "3716991",
            "3716992",
            "9157",
            "236240",
            "26058",
            "591409",
            "2102",
            "130217",
            "15342",
            "3716993",
            "38158",
            "730751",
            "137169",
            "3716994",
            "401471",
            "836486",
            "30294",
            "3716995",
            "47560",
            "450604",
            "2146",
            "694402",
            "123071",
            "3716996",
            "117653",
            "396267",
            "45686"
        ],
        "cited_paper_data": [{
            "url": "http://citeseerx.ist.psu.edu/viewdoc/similar?doi=10.1.1.20.1673&type=sc",
            "title": "Some Dummy title ",
            "Author": "Geoffrey Hinton, Luke Skywalker",
            "Year": "2015"
        }],
        "doi": "10.1.1.61.2545",
        "title": "Wireless mesh networks: a survey."
    })
