# Biscoitinho Político

O Projeto Biscoitinho Político utiliza impressoras térmicas (aquelas de nota fiscal) padrão para imprimir
bits de informaçṍes políticas.

O sistema é composto de 3 partes:
1) Parser
    O Parser - escrito em python - processa, agrega e converte as informações do orçamento de minas gerais para um formato JSON mais palatavel.
    Dependências:
        Python 2.6
        CSVKit
2) Server
    O Server - escrito em python - utiliza o framework Flask para servir o conteúdo bruto que vai ser requisitado pela impressora. 
    Dependências:
        Python 2.6
        Flask
3) Arduino
    A comunicação com a impressora é feita através de um arduino conectado na rede. Para isso utilizamos um Shield Ethernet padrão. No momento as configurações do servidor estão hard-coded no sketch.
    Dependências:
        Arduino 1.0.1
        Ethernet.h
        SPI.h
        SoftwareSerial.h

Além disso você vai precisar de uma impressora térmica capaz de se comunicar via serial.
