# Virtualizzazione di un Sistema SCADA con OPC UA

## Introduzione
La virtualizzazione dei sistemi SCADA (Supervisory Control and Data Acquisition) sta diventando una pratica sempre più comune per garantire la gestione, il monitoraggio e il controllo efficiente di processi industriali complessi. In questo progetto, abbiamo implementato un sistema SCADA virtualizzato per il controllo e il monitoraggio del sistema di condizionamento di un deposito agroalimentare. La soluzione si basa sul protocollo **OPC UA**, che rappresenta uno degli standard più utilizzati nell'automazione industriale per garantire la comunicazione sicura e interoperabile tra dispositivi e sistemi di controllo.

Il presente documento descrive nel dettaglio il processo di virtualizzazione del sistema SCADA, l'architettura utilizzata, la configurazione del server e della dashboard HMI (Human-Machine Interface), e le funzionalità specifiche del protocollo OPC UA. Vengono illustrati anche i vari componenti implementati, il loro scopo e il modo in cui contribuiscono all'intero sistema.

## Architettura del Sistema
Il sistema di condizionamento virtualizzato è composto dai seguenti elementi principali:

1. **Server OPC UA**: Simula i sensori di temperatura e le unità di condizionamento dell'aria. Comunica con il resto del sistema tramite il protocollo OPC UA.
2. **Client Flask**: Funziona come interfaccia HMI, che consente agli utenti di monitorare lo stato del sistema e interagire con le unità di condizionamento tramite una dashboard web.
3. **Dashboard Web**: Interfaccia grafica costruita con HTML, CSS e JavaScript che permette il controllo manuale delle unità di condizionamento e il monitoraggio delle temperature.

### Server OPC UA
Il **server OPC UA** rappresenta il cuore del sistema SCADA. È stato creato utilizzando la libreria `opcua` in Python, che permette di configurare i nodi del server in modo flessibile. In particolare, il server implementa:

- **Sensori di Temperatura**: Sono stati creati 10 nodi variabili per simulare i 10 sensori di temperatura presenti nelle varie aree del deposito. Ogni sensore è inizializzato con una temperatura di 25°C e varia nel range tra **8°C** e **25°C**, a seconda dello stato dei condizionatori.
- **Unità di Condizionamento**: Sono presenti 10 nodi variabili che rappresentano lo stato di ciascun condizionatore (ON/OFF). Lo stato di ogni condizionatore viene inizializzato a `OFF` e può essere modificato manualmente dall'utente attraverso la dashboard web.
- **Allarmi Critici**: Viene monitorato se la temperatura di uno o più sensori supera la soglia critica di **12°C**. In caso positivo, viene attivato un allarme critico che viene mostrato sulla dashboard.

Le temperature dei sensori cambiano dinamicamente in funzione dello stato dei condizionatori. Quando un condizionatore è **ON**, la temperatura associata diminuisce di 1°C (fino a un minimo di 8°C), mentre quando è **OFF**, la temperatura aumenta di 1°C (fino a un massimo di 25°C). Questa logica è stata implementata per simulare realisticamente il comportamento del sistema di condizionamento.

### Dashboard Web e Client Flask
La **dashboard web** è stata costruita utilizzando **Flask** per la parte di backend, HTML e CSS per la parte di frontend, e JavaScript per la gestione dell'aggiornamento automatico della pagina.

- **Controllo delle Unità di Condizionamento**: Ogni unità di condizionamento può essere accesa o spenta direttamente dalla dashboard. Questo è stato realizzato tramite una **sezione di controllo** nella quale sono presenti pulsanti "Accendi" e "Spegni" per ciascun condizionatore.
- **Aggiornamento Automatico della Dashboard**: La dashboard si aggiorna automaticamente ogni 5 secondi per garantire che gli utenti abbiano sempre una visione aggiornata delle temperature e degli stati delle unità di condizionamento. Questo comportamento è stato implementato tramite uno script JavaScript che ricarica la pagina a intervalli regolari.
- **Allarmi Critici**: Quando una temperatura supera i 12°C, il relativo sensore viene visualizzato con uno sfondo rosso e viene mostrato un messaggio di allarme critico. Questo permette agli utenti di identificare rapidamente le aree del deposito che necessitano di attenzione.

## Protocollo OPC UA
**OPC UA** (Open Platform Communications Unified Architecture) è un protocollo di comunicazione standard ampiamente adottato in ambito industriale. Per questo progetto, OPC UA è stato scelto per i seguenti motivi:

- **Interoperabilità**: OPC UA è progettato per essere agnostico rispetto alla piattaforma, consentendo la comunicazione tra dispositivi e sistemi eterogenei.
- **Sicurezza**: OPC UA integra meccanismi di sicurezza come l'autenticazione, l'autorizzazione e la crittografia, garantendo che le comunicazioni siano sicure.
- **Modello di Dati Flessibile**: OPC UA consente la rappresentazione di dati complessi tramite una struttura a nodi. Questo è stato utile per modellare il sistema SCADA con nodi per ogni sensore e ogni condizionatore.

Il server OPC UA è stato realizzato in Python utilizzando la libreria **python-opcua**, che ha permesso di creare nodi per i sensori e le unità di condizionamento, impostare e leggere valori, e gestire eventi di allarme.

## Flusso di Lavoro e Implementazione
1. **Configurazione del Server OPC UA**: Il server OPC UA è stato configurato per rappresentare i sensori di temperatura e le unità di condizionamento come variabili scrivibili. Ogni sensore è inizializzato con una temperatura di 25°C e la logica per la variazione delle temperature è stata integrata nel ciclo principale del server.
2. **Creazione della Dashboard HMI con Flask**: La dashboard HMI è stata sviluppata utilizzando Flask. Il server Flask si connette al server OPC UA e recupera in tempo reale i valori delle temperature e degli stati dei condizionatori, presentandoli agli utenti.
3. **Aggiornamento e Controllo**: La dashboard consente sia di visualizzare i dati che di controllare lo stato delle unità di condizionamento. Ogni volta che un utente interagisce con la dashboard, viene inviata una richiesta POST al server Flask, che aggiorna lo stato del condizionatore corrispondente sul server OPC UA.

## Vantaggi della Virtualizzazione
La virtualizzazione di un sistema SCADA tramite OPC UA offre numerosi vantaggi:
- **Riduzione dei Costi**: Non sono necessari costosi dispositivi fisici per sperimentare e testare il sistema SCADA. Tutto può essere simulato e controllato in un ambiente virtuale.
- **Sicurezza e Monitoraggio Remoto**: La virtualizzazione consente il monitoraggio e il controllo remoto, migliorando la sicurezza del deposito e riducendo la necessità di presenza fisica.
- **Scalabilità**: Con OPC UA, è possibile aggiungere nuovi sensori, dispositivi e logiche di controllo senza apportare modifiche sostanziali all'infrastruttura del sistema.

## Conclusioni
In questo progetto, la virtualizzazione di un sistema SCADA per il controllo del condizionamento di un deposito agroalimentare è stata implementata con successo utilizzando **OPC UA**. La soluzione consente il monitoraggio e il controllo remoto del sistema di condizionamento, con una logica realistica per la gestione delle temperature in funzione dello stato delle unità di condizionamento.

L'uso del protocollo OPC UA ha garantito un'integrazione sicura e flessibile, permettendo una facile comunicazione tra il server SCADA e la dashboard HMI. Questa infrastruttura virtualizzata non solo facilita il controllo efficiente del deposito, ma rappresenta anche un esempio di come sia possibile innovare utilizzando tecnologie moderne per l'automazione industriale.

Se si desiderano ulteriori sviluppi, come l'integrazione con sistemi di notifica automatizzati o l'adozione di tecniche di intelligenza artificiale per il controllo predittivo, il sistema descritto rappresenta una solida base da cui partire.


