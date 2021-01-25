#!/usr/bin/env python
import sys,os
import numpy as np

os.environ["LHAPDF_DATA_PATH"] = os.getcwd()

import lhapdf
import argparse
#--matplotlib
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
matplotlib.rc('text',usetex=True)
from matplotlib.ticker import MultipleLocator
import pylab  as py

#--index conventions:
#--1: down
#--2: up
#--3: strange
#--4: charm
#--5: bottom
#--6: top
#--21: gluon
#--negative values for antiquarks


#--908: F2   (NC F2) 
#--909: FL   (NC FL) 
#--910: F3   (NC F3) 
#--930: W2m  (CC F2^{W-}) 
#--931: WLm  (CC FL^{W-})
#--932: W3m  (CC F3^{W-})
#--940: W2p  (CC F2^{W+})
#--941: WLp  (CC FL^{W+})
#--942: W3p  (CC F3^{W+})

#--mode 0: plot each replica
#--mode 1: plot average and standard deviation of replicas

X1=10**np.linspace(-4,-1)
X2=np.linspace(0.101,0.99)
X=np.append(X1,X2)

def plot_pdfs(Q2,mode=0):

    nrows,ncols=3,2
    fig = py.figure(figsize=(ncols*7,nrows*4))
    ax11=py.subplot(nrows,ncols,1)
    ax12=py.subplot(nrows,ncols,2)
    ax21=py.subplot(nrows,ncols,3)
    ax22=py.subplot(nrows,ncols,4)
    ax31=py.subplot(nrows,ncols,5)
    ax32=py.subplot(nrows,ncols,6)

    hand = {}

    PDF = lhapdf.mkPDFs('JAM21PDF-PDF_proton_nlo')
    nrep = len(PDF)

    flavs = ['uv','dv','g','db+ub','db-ub','s+sb','Rs']
    data = {flav: [] for flav in flavs} 

    for i in range(nrep):
        d =  np.array([PDF[i].xfxQ2( 1,x,Q2) for x in X])
        u =  np.array([PDF[i].xfxQ2( 2,x,Q2) for x in X])
        s =  np.array([PDF[i].xfxQ2( 3,x,Q2) for x in X])
        db = np.array([PDF[i].xfxQ2(-1,x,Q2) for x in X])
        ub = np.array([PDF[i].xfxQ2(-2,x,Q2) for x in X])
        sb = np.array([PDF[i].xfxQ2(-3,x,Q2) for x in X])
        g  = np.array([PDF[i].xfxQ2(21,x,Q2) for x in X])
        data['uv'].append(u-ub)
        data['dv'].append(d-db)
        data['g'] .append(g)
        data['db+ub'].append(db+ub)
        data['db-ub'].append(db-ub)
        data['s+sb'].append(s+sb)
        data['Rs'].append((s+sb)/(db+ub))
        
    for flav in data:

        if flav=='uv' or flav=='dv': ax = ax11
        elif flav=='g':              ax = ax12
        elif flav=='db+ub':          ax = ax21
        elif flav=='db-ub':          ax = ax22
        elif flav=='s+sb':           ax = ax31
        elif flav=='Rs':             ax = ax32

        mean = np.mean(data[flav],axis=0)
        std = np.std(data[flav],axis=0)

        if mode==0:
            for i in range(nrep):

                if flav=='g': data[flav][i] /= 10.0

                hand['JAM21'] ,= ax.plot(X,data[flav][i],color='red',alpha=0.1)
 
        #--plot average and standard deviation
        if mode==1:
            if flav=='g':
                mean /= 10.0
                std  /= 10.0

            where = [1 for i in range(len(X))]
            if flav=='Rs':
                where = []
                for x in X:
                    if x < 0.2: where.append(1)
                    if x > 0.2: where.append(0)

            hand['JAM21']  = ax.fill_between(X,mean-std,mean+std,color='red',alpha=0.9,where=where)


    for ax in [ax11,ax12,ax21,ax22,ax31,ax32]:
          ax.set_xlim(1e-2,1)
          ax.semilogx()
            
          ax.tick_params(axis='both', which='major', top=True, right=True, direction='in',labelsize=30,length=10)
          ax.tick_params(axis='both', which='minor', top=True, right=True, direction='in',labelsize=30,length=5)
          ax.set_xticks([0.01,0.1,1])
          ax.set_xticklabels([r'$0.01$',r'$0.1$',r'$1$'])

    ax11.tick_params(axis='both', which='both', labelbottom=False)
    ax12.tick_params(axis='both', which='both', labelbottom=False)
    ax21.tick_params(axis='both', which='both', labelbottom=False)
    ax22.tick_params(axis='both', which='both', labelbottom=False)

    ax11.set_ylim(0,0.7)
    ax12.set_ylim(0,0.5)
    ax21.set_ylim(-0.05,0.7)
    ax22.set_ylim(-0.04,0.08)
    ax31.set_ylim(0,0.7)
    ax32.set_ylim(0,1.2)

    ax11.set_yticks([0.2,0.4,0.6])
    ax12.set_yticks([0.2,0.4])
    ax21.set_yticks([0,0.2,0.4,0.6])
    ax22.set_yticks([-0.02,0,0.02,0.04,0.06])
    ax31.set_yticks([0.2,0.4,0.6])
    ax32.set_yticks([0.5,1.0])

    minorLocator = MultipleLocator(0.05)
    ax11.yaxis.set_minor_locator(minorLocator)
    ax12.yaxis.set_minor_locator(minorLocator)
    ax21.yaxis.set_minor_locator(minorLocator)
    ax31.yaxis.set_minor_locator(minorLocator)
    minorLocator = MultipleLocator(0.005)
    ax22.yaxis.set_minor_locator(minorLocator)
    minorLocator = MultipleLocator(0.1)
    ax32.yaxis.set_minor_locator(minorLocator)

    for ax in [ax31,ax32]:
        ax.set_xlabel(r'\boldmath$x$' ,size=30)
        ax.xaxis.set_label_coords(0.80,0.00)

    ax11.text(0.85 ,0.50  ,r'\boldmath{$xu_{v}$}'            , transform=ax11.transAxes,size=30)
    ax11.text(0.60 ,0.20  ,r'\boldmath{$xd_{v}$}'            , transform=ax11.transAxes,size=30)
    ax12.text(0.65 ,0.25  ,r'\boldmath{$xg/10$}'             , transform=ax12.transAxes,size=30)
    ax21.text(0.10 ,0.20  ,r'\boldmath{$x(\bar{d}+\bar{u})$}', transform=ax21.transAxes,size=30)
    ax22.text(0.20 ,0.10  ,r'\boldmath{$x(\bar{d}-\bar{u})$}', transform=ax22.transAxes,size=30)
    ax31.text(0.50 ,0.40  ,r'\boldmath{$x(s+\bar{s})$}',       transform=ax31.transAxes,size=30)
    ax32.text(0.05 ,0.05  ,r'\boldmath{$R_s$}',       transform=ax32.transAxes,size=30)

    if Q2 == 1.27**2: ax12.text(0.05,0.08,r'$Q^2 = m_c^2$'                                  , transform=ax12.transAxes,size=30)
    else:             ax12.text(0.05,0.08,r'$Q^2 = %s$'%Q2 + ' ' + r'\textrm{GeV}' + r'$^2$', transform=ax12.transAxes,size=30)

    ax21.axhline(0.0,ls='--',color='black',alpha=0.5)
    ax22.axhline(0.0,ls='--',color='black',alpha=0.5)
    ax32.axvline(0.2,ls='--',color='black',alpha=0.5)

    handles,labels = [],[]
    handles.append(hand['JAM21'])
    labels.append(r'\textbf{\textrm{JAM21}}')
    ax11.legend(handles,labels,loc='upper left',  fontsize = 28, frameon = 0, handletextpad = 0.3, handlelength = 1.0)

    py.tight_layout()
    py.subplots_adjust(hspace = 0, wspace = 0.20)

    filename = 'gallery/pdfs'
    if mode==1: filename += '-bands'
    filename+='.png'

    py.savefig(filename)
    py.clf()
    print ('Saving figure to %s'%filename)

def plot_ht(mode=0):

    nrows,ncols=1,1
    fig = py.figure(figsize=(ncols*8,nrows*5))
    ax11 = py.subplot(nrows,ncols,1) 

    hand = {}


    #--collect data from different groups
    Q2 = 10
    data = {}
    for tar in ['p','n']:
        data[tar] = []
        if tar == 'p': tabname, color = 'JAM21PDF-HT_proton' , 'firebrick'
        if tar == 'n': tabname, color = 'JAM21PDF-HT_neutron', 'darkgreen'
        HT = lhapdf.mkPDFs(tabname)
        nrep = len(HT)
        for i in range(nrep):
            ht = np.array([HT[i].xfxQ2(908,x,Q2) for x in X])
            data[tar].append(ht)

        if mode == 0:
            for i in range(nrep):
                hand[tar] ,= ax11.plot(X,data[tar][i],color=color,alpha=0.1)

        if mode == 1:
            mean = np.mean(np.array(data[tar]),axis=0)
            std  = np.std (np.array(data[tar]),axis=0)
            hand[tar] = ax11.fill_between(X,mean-std,mean+std,color=color,alpha=0.9)
        

    h0 =-3.2874
    h1 = 1.9274
    h2 =-2.0701
    ht = h0*X**h1*(1+h2*X)
    hand['CJ15'] ,= ax11.plot(X,ht,'b--')

    ax11.set_ylim(-0.4,2)

    ax11.text(0.05,0.25,r'\boldmath$H^N$',transform=ax11.transAxes,size=40)

    ax11.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=30)

    ax11.set_xlim(0,1)
    ax11.set_xlabel(r'\boldmath$x$',size=30)
    ax11.xaxis.set_label_coords(0.95,0.00)

    ax11.axhline(0,0,1,ls='--',color='black',alpha=0.5)

    ax11.text(0.75,0.05,r'\textbf{\textrm{AOT}}',size=30,transform=ax11.transAxes)

    for ax in [ax11]:
        minorLocator = MultipleLocator(0.1)
        majorLocator = MultipleLocator(0.5)
        ax.yaxis.set_minor_locator(minorLocator)
        ax.yaxis.set_major_locator(majorLocator)
        minorLocator = MultipleLocator(0.02)
        majorLocator = MultipleLocator(0.2)
        ax.xaxis.set_minor_locator(minorLocator)
        ax.xaxis.set_major_locator(majorLocator)
        ax.xaxis.set_tick_params(which='major',length=6)
        ax.xaxis.set_tick_params(which='minor',length=3)
        ax.yaxis.set_tick_params(which='major',length=6)
        ax.yaxis.set_tick_params(which='minor',length=3)

    ax11.set_xticks([0,0.2,0.4,0.6,0.8])

    handles,labels = [],[]
    handles.append(hand['p'])
    handles.append(hand['n'])
    handles.append(hand['CJ15'])
    labels.append(r'\textbf{\textrm{JAM21 (p)}}')
    labels.append(r'\textbf{\textrm{JAM21 (n)}}')
    labels.append(r'\textbf{\textrm{CJ15}}')

    ax11.legend(handles,labels,frameon=False,loc=2,fontsize=25, handletextpad = 0.5, handlelength = 1.5)

    py.tight_layout()

    filename = 'gallery/ht'
    if mode == 1: filename += '-bands'
    filename += '.png'
    py.savefig(filename)
    py.clf()
    print('Saving figure to %s'%filename)

def plot_off(Q2,mode=0):

    nrows,ncols=1,1
    fig = py.figure(figsize=(ncols*8,nrows*5))
    ax11 = py.subplot(nrows,ncols,1)

    hand = {}

    OFF = lhapdf.mkPDFs('JAM21PDF-offshell')
    nrep = len(OFF)

    data = [] 

    for i in range(nrep):
        off =  np.array([OFF[i].xfxQ2(908,x,Q2) for x in X])
        data.append(off)

    if mode==0:
        for i in range(nrep):
            hand['JAM21'] ,= ax11.plot(X,data[i],color='red',alpha=0.1)

    if mode == 1:
        mean = np.mean(np.array(data),axis=0)
        std  = np.std(np.array(data),axis=0)
        hand['JAM21'] = ax11.fill_between(X,mean-std,mean+std,color='red',alpha=0.9,)

    
    #--CJ15 
    C =-3.6735
    x0= 5.7717e-2
    x1=0.36419
    dfcj=C*(X-x0)*(X-x1)*(1+x0-X)
    hand['CJ'] ,= ax11.plot(X,dfcj,'b--')
    #--KP 
    C = 8.10
    x0= 0.448
    x1= 0.05
    dfcj=C*(X-x0)*(X-x1)*(1+x0-X)
    hand['KP'] ,= ax11.plot(X,dfcj,'g--')

    ax11.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=30)

    ax11.text(0.60,0.05,r'$Q^2=%s{\rm~GeV^2}$'%Q2,size=30,transform=ax11.transAxes)

    ax11.set_ylim(-1.2,1.2)
    ax11.set_xlim(0,1)
    ax11.text(0.05,0.05,r'\boldmath$\delta f^0$',transform=ax11.transAxes,size=40)
    ax11.set_xlabel(r'\boldmath$x$'         ,size=30)
    ax11.xaxis.set_label_coords(0.95,0.00)

    ax11.axhline(0,alpha=0.5,color='k',ls='--')

 
    for ax in [ax11]:
        minorLocator = MultipleLocator(0.1)
        majorLocator = MultipleLocator(0.5)
        ax.yaxis.set_minor_locator(minorLocator)
        ax.yaxis.set_major_locator(majorLocator)
        minorLocator = MultipleLocator(0.02)
        majorLocator = MultipleLocator(0.2)
        ax.xaxis.set_minor_locator(minorLocator)
        ax.xaxis.set_major_locator(majorLocator)
        ax.xaxis.set_tick_params(which='major',length=6)
        ax.xaxis.set_tick_params(which='minor',length=3)
        ax.yaxis.set_tick_params(which='major',length=6)
        ax.yaxis.set_tick_params(which='minor',length=3)
        ax.set_xticks([0,0.2,0.4,0.6,0.8])


    handles,labels=[],[]
    handles.append(hand['JAM21'])
    handles.append(hand['CJ'])
    handles.append(hand['KP'])
    labels.append(r'\textbf{\textrm{JAM21}}')
    labels.append(r'\textbf{\textrm{CJ15}}')
    labels.append(r'\textbf{\textrm{KP}}')

    ax11.legend(handles,labels,frameon=False,loc='upper left',fontsize=28, handletextpad = 0.5, handlelength = 1.5, ncol = 1, columnspacing = 0.5)

    py.tight_layout()

    filename = 'gallery/off'
    if mode == 1: filename += '-bands'
    filename += '.png'
    print('Saving figures to %s'%filename)
    py.savefig(filename)
    py.clf()

def plot_stf(Q2,mode=0):

    nrows,ncols=1,3
    fig = py.figure(figsize=(ncols*7,nrows*4))
    ax11=py.subplot(nrows,ncols,1)
    ax12=py.subplot(nrows,ncols,2)
    ax13=py.subplot(nrows,ncols,3)

    hand = {}


    stfs = ['F2','FL','F3']
    data = {}
    data['p'] = {stf: [] for stf in stfs} 

    for tar in data:
        if tar == 'p': tablename = 'JAM21PDF-STF_proton'
        if tar == 'd': tablename = 'JAM21PDF-STF_deuteron'
        STF = lhapdf.mkPDFs(tablename)
        nrep = len(STF)
        for i in range(nrep):
            F2 =  np.array([STF[i].xfxQ2(908,x,Q2)*x for x in X])
            FL =  np.array([STF[i].xfxQ2(909,x,Q2)*x for x in X])
            F3 =  np.array([STF[i].xfxQ2(910,x,Q2)*x for x in X])
            data['p']['F2'].append(F2)
            data['p']['FL'].append(FL)
            data['p']['F3'].append(F3)

        for stf in data[tar]:
            mean = np.mean(data[tar][stf],axis=0)
            std = np.std(data[tar][stf],axis=0)

            if tar=='p':   color='firebrick'
            elif tar=='d': color='darkcyan'

            if stf =='F2':   ax = ax11
            elif stf =='FL': ax = ax12
            elif stf =='F3': ax = ax13

            #--plot each replica
            if mode==0:
                for i in range(nrep):
                    hand[tar] ,= ax.plot(X,data[tar][stf][i],color=color,alpha=0.1)
      
            #--plot average and standard deviation
            if mode==1:
                hand[tar] = ax.fill_between(X,mean-std,mean+std,color=color,alpha=0.5)


    for ax in [ax11,ax12,ax13]:
          ax.set_xlim(1e-4,1)
          ax.semilogx()
            
          ax.tick_params(axis='both', which='both', top=True, right=True, direction='in',labelsize=20)
          ax.set_xticks([0.0001,0.001,0.01,0.1,1])
          ax.set_xticklabels([r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$',r'$1$'])

    ax11.set_ylim(0,0.1)   
    ax12.set_ylim(0,0.004) 
    ax13.set_ylim(0,0.0004)

    ax11.set_xlabel(r'$x$' ,size=35)
    ax12.set_xlabel(r'$x$' ,size=35)   
    ax13.set_xlabel(r'$x$' ,size=35)   

    if Q2 == 1.27**2: ax11.text(0.40,0.85,r'$Q^2 = m_c^2$'                                  , transform=ax11.transAxes,size=30)
    else:             ax11.text(0.40,0.85,r'$Q^2 = %s$'%Q2 + ' ' + r'\textrm{GeV}' + r'$^2$', transform=ax11.transAxes,size=30)

    ax11.text(0.05,0.85,r'\boldmath$xF_2$',transform=ax11.transAxes,size=30)
    ax12.text(0.05,0.85,r'\boldmath$xF_L$',transform=ax12.transAxes,size=30)
    ax13.text(0.05,0.85,r'\boldmath$xF_3$',transform=ax13.transAxes,size=30)

    handles,labels=[],[]
    handles.append(hand['p'])
    #handles.append(hand['d'])
    labels.append(r'\boldmath$p$')
    #labels.append(r'\boldmath$d$')
    ax11.legend(handles,labels,frameon=False,loc='lower left',fontsize=28, handletextpad = 0.5, handlelength = 1.5, ncol = 1, columnspacing = 0.5)

    py.tight_layout()

    filename = 'gallery/stfs'
    if mode==1: filename += '-bands'
    filename+='.png'

    py.savefig(filename)
    print ('Saving figure to %s'%filename)
    py.clf()

def plot_CCstf(Q2,mode=0):

    nrows,ncols=1,3
    fig = py.figure(figsize=(ncols*7,nrows*4))
    ax11=py.subplot(nrows,ncols,1)
    ax12=py.subplot(nrows,ncols,2)
    ax13=py.subplot(nrows,ncols,3)

    hand = {}

    stfs = ['W2+','WL+','W3+','W2-','WL-','W3-']
    data = {stf: [] for stf in stfs} 

    tablename = 'JAM21PDF-STF_proton'
    STF = lhapdf.mkPDFs(tablename)
    nrep = len(STF)

    for i in range(nrep):
        W2m =  np.array([STF[i].xfxQ2(930,x,Q2)*x for x in X])
        WLm =  np.array([STF[i].xfxQ2(931,x,Q2)*x for x in X])
        W3m =  np.array([STF[i].xfxQ2(932,x,Q2)*x for x in X])
        W2p =  np.array([STF[i].xfxQ2(940,x,Q2)*x for x in X])
        WLp =  np.array([STF[i].xfxQ2(941,x,Q2)*x for x in X])
        W3p =  np.array([STF[i].xfxQ2(942,x,Q2)*x for x in X])
        data['W2+'].append(W2p)
        data['WL+'].append(WLp)
        data['W3+'].append(W3p)
        data['W2-'].append(W2m)
        data['WL-'].append(WLm)
        data['W3-'].append(W3m)

    for stf in data:
        mean = np.mean(data[stf],axis=0)
        std = np.std(data[stf],axis=0)

        if stf[-1]=='+': color='firebrick'
        if stf[-1]=='-': color='darkcyan'

        if stf =='W2+':   ax = ax11
        elif stf =='WL+': ax = ax12
        elif stf =='W3+': ax = ax13
        elif stf =='W2-': ax = ax11
        elif stf =='WL-': ax = ax12
        elif stf =='W3-': ax = ax13
        else: continue

        #--plot each replica
        if mode==0:
            for i in range(nrep):
                hand[stf[-1]] ,= ax.plot(X,data[stf][i],color=color,alpha=0.1)
    
        #--plot average and standard deviation
        if mode==1:
            hand[stf[-1]] = ax.fill_between(X,mean-std,mean+std,color=color,alpha=0.9)


    for ax in [ax11,ax12,ax13]:
          ax.set_xlim(1e-4,1)
          ax.semilogx()
            
          ax.tick_params(axis='both', which='both', top=True, right=True, direction='in',labelsize=20)
          ax.set_xticks([0.0001,0.001,0.01,0.1,1])
          ax.set_xticklabels([r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$',r'$1$'])


    ax13.axhline(0,0,1,ls='--',color='black',alpha=0.5)

    ax11.set_ylim(0,0.4)   
    ax12.set_ylim(0,0.015) 
    ax13.set_ylim(-1.0,2.0)

    ax11.set_xlabel(r'$x$' ,size=35)
    ax12.set_xlabel(r'$x$' ,size=35)   
    ax13.set_xlabel(r'$x$' ,size=35)   

    if Q2 == 1.27**2: ax11.text(0.40,0.85,r'$Q^2 = m_c^2$'                                  , transform=ax11.transAxes,size=30)
    else:             ax11.text(0.40,0.85,r'$Q^2 = %s$'%Q2 + ' ' + r'\textrm{GeV}' + r'$^2$', transform=ax11.transAxes,size=30)

    ax11.text(0.05,0.85,r'\boldmath$xW_2$',transform=ax11.transAxes,size=30)
    ax12.text(0.05,0.85,r'\boldmath$xW_L$',transform=ax12.transAxes,size=30)
    ax13.text(0.05,0.85,r'\boldmath$xW_3$',transform=ax13.transAxes,size=30)

    handles,labels=[],[]
    handles.append(hand['+'])
    handles.append(hand['-'])
    labels.append(r'\boldmath$W^+$')
    labels.append(r'\boldmath$W^-$')
    ax11.legend(handles,labels,frameon=False,loc='lower left',fontsize=28, handletextpad = 0.5, handlelength = 1.5, ncol = 1, columnspacing = 0.5)

    py.tight_layout()

    filename = 'gallery/stfs-CC'
    if mode==1: filename += '-bands'
    filename+='.png'
    py.savefig(filename)
    print ('Saving figure to %s'%filename)
    py.clf()


if __name__=="__main__":

    Q2   = 10
    mode = 1

    plot_CCstf(Q2,mode=mode)
    sys.exit()

    plot_pdfs(Q2,mode=mode)
    plot_ht(mode=mode)
    plot_off(Q2,mode=mode)
    #--need to add deuteron
    plot_stf(Q2,mode=mode)
    plot_CCstf(Q2,mode=mode)












