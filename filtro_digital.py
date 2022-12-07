def filtro_digital(pdc,nf,original_data,filtertype = 'low'):
    '''    
    FUNÇÃO PARA CRIAÇÃO DE FILTRO DIGITAL EM PYTHON
    Igual a Matlab: funções butter+freqz+filtfilt
    ***
    pdc: int (Periodo de corte)
        Para filtrar com base no período, uma abordagem melhor para estudo de fenomenos de escala temporal de horas ou dias.
        EXEMPLO: Se tivermos 4 dados por dia e queremos atenuar 
        todas as oscilações com período menor que 3 dias (com o filtro 'low'), então usamos pdc = 3*4
        Se o dado for amostragem diária, então basta usar pdc = 3. 
        
    nf: int (Numero de pesos final - Ordem final do filtro)
        Testar valores para não ocorrer o Fenômeno de Gibbs: observar na figura.
        Se a ordem for muito grande, o filtro vai estourar. Se ocorrer reduzir o valor de nf.
        Exemplo: começar com nf = 20 para um dado de amostragem diária
        
    filtertype: 'low','high'
        'low' for lowpass filter
        'high' for highpass filter
        
    original_data: pd.DataFrame or np.array (preferences)
        The data you want to filter

    ***
    
    '''
    
    import matplotlib.pyplot as plt
    from pandas import DataFrame as DF
    from scipy.signal import butter, filtfilt,freqz
    np.seterr(divide='ignore', invalid='ignore')

    font_size = 14
    pi = np.pi

    pdc = pdc
    fc = 1/pdc #FREQUENCIA DE CORTE
    fn = 1/2 
    #fc/fn #FREQUENCIA DE CORTE NORMALIZADA

    #----------------------------------CRIAÇÃO DO FILTRO

    plt.figure(dpi=60)
    plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0.1, 1, nf)))) #PARA PLOT EM ESCALA DE COR

    for n in range(1,nf):
        b, a = butter(N = n, 
                      Wn = fc/fn, #CUTTOF FREQUENCY #IF Wn IS A 2 ELEMENT VECTOR, RETURNS AN ORDER 2N BANDPASS FILTER W1<W<W2
                      btype = filtertype)#'low' : LOWPASS
        wl, hl = freqz(b, a) #CALCULA A RESPOSTA EM FREQUENCIA DO FILTRO BUTTER
        plt.semilogx(1/(fn*wl/pi) , abs(hl))

    plt.semilogx(1/(fn*wl/pi) , abs(hl) ,color='k') #ULTIMA CURVA, SERÁ O FILTRO IDEAL; EIXO X EM PERIODO
    #plt.semilogx((fn*wl/pi) , abs(hl) ,color='k')   #ULTIMA CURVA, SERÁ O FILTRO IDEAL; EIXO X EM FREQUENCIA (ROTAÇÕES POR [UNIDADE DE MEDIDA DO PERIODO])

    plt.xlabel('Period [PERIOD UNIT OF MEASUREMENT]',fontsize=font_size)
    plt.ylabel('Gain [WITHOUT DIMENSION]',fontsize=font_size)
    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)

    ##----------------------------------FILTRANDO O DADO
    #
    original_data = DF(original_data)
    filtered_data = filtfilt(b, a, original_data,axis=0, padtype='odd', padlen=3*(max(len(b),len(a))-1))
    filtered_data = DF(filtered_data,index=original_data.index)
    #
    ##----------------------------------RESULTADO
    #
    plt.figure(figsize=(17.5 , 5))
    plt.plot(original_data,color='gray',label = 'ORIGINAL DATA')
    plt.plot(filtered_data,color='k',label = 'FILTERED DATA')
    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.legend()
    
    return filtered_data

#------------------------
#RUNNING LOWPASS:
#######filtro_digital(pdc=3*4,nf=20,original_data=x,filtertype='low')