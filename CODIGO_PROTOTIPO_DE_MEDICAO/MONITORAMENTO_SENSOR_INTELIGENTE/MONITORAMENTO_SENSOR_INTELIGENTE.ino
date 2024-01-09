#include<EEPROM.h>
#include<WiFi.h>
#define FLAG_FLASH_INICIALIZADA 9
#define INTERRUPCAO_SENSOR 17
#define led 5


//Bibliotecas para o FireBase
#include<Arduino.h>
#include<Firebase_ESP_Client.h>
#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"
#define API_KEY "AIzaSyDXa_7INUUVwo34q0cA0Ob28TAac9iM9JA"
#define DATABASE_URL "https://teste-2367e-default-rtdb.firebaseio.com/"

unsigned long  CONTADOR_PULSOS = 0;
uint64_t CONTADOR_LITROS = 0;
uint64_t  QUANTIDADE_LITROS_ANTIGA; //Inicializada com lixo
uint64_t  VALOR_MAXIMO_LITROS = 18446744073709551600;
const char* WIFI_SSID  = "COLOQUE_A_REDE"; //Rede 
const char* WIFI_PASSWORD  = "COLOQUE_A_SENHA_DA_REDE"; //Senha do wifi 
const char* CAMINHO = "Enderecos/58088140-191/Litros";

bool signupOK = false;
//Define Firebase Data object
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

void setup() {
  //Inicia a EEPROM com o tamnho de 5 bytes (minimo).
  EEPROM.begin(10); // 10 POSIÇÕES INICIALIZADAS NA EEPROM
  Serial.begin(9600);
  //Conecta a rede
  WiFi.begin(WIFI_SSID , WIFI_PASSWORD );
 //Testando se o status do WiFi está conectado 
  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.println("Connecting to WiFi.."); //conectando ao wifi
    }
  Serial.println("Connected to the WiFi network"); //conectado a rede

  //Chave API e URL para Firebase
  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;

    /* Sign up */
  if (Firebase.signUp(&config, &auth, "", "")){
    Serial.println("ok");
    signupOK = true;
  }
  else{
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }
  //
  // Entrará uma única vez, neste IF.
  // Se não existir o número escolhido(9) na posição ZERO, irá grava-lo. Isto é necessário para evitar gravações desnecessárias!
  if(EEPROM.read(0) != FLAG_FLASH_INICIALIZADA){//  // FLAG_FLASH_INICIALIZADA = 9
      //Escreve no endereço 0, o valor FLAG_FLASH_INICIALIZADA!
    //if(1){ // utilizado pra zerar a EEPROM
      EEPROM.put(0, FLAG_FLASH_INICIALIZADA); 
      EEPROM.commit();
      // Salva o dado na EEPROM, a partir da 1 posição até a 8. Esta váriavel ocupa 8 bytes!
      EEPROM.put(1, (uint64_t)0); //
      EEPROM.commit();
    }
  else{
    //PEGANDO O VALOR QUE FOI SALVO ANTERIORMENTE NA POSIÇÃO 1 A 8 DA EEPROM, JA QUE A POSIÇÃO ZERO ESTÁ PREENCHIDA COM FLAG_FLASH_INICIALIZADA!
      EEPROM.get(1, CONTADOR_LITROS); 
     }
  //Substituindo o valor que era lixo, pela quantidade de litros salva até aqui!   
  QUANTIDADE_LITROS_ANTIGA = CONTADOR_LITROS;
  //Declarando o pino da Interrupção e pino do led!
  pinMode(INTERRUPCAO_SENSOR, INPUT);
  pinMode(led, OUTPUT);
  //Declarando a Interrupção em caso de pulso!
  attachInterrupt(digitalPinToInterrupt(INTERRUPCAO_SENSOR),PULSOS, RISING); 
  //FireBase
  //Atribua a função de retorno de chamada para a tarefa de geração de token de longa duração
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h
  
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void loop() {
  // Se WiFi estiver conectado, deixar o led verde ligado.
  if(WiFi.status() == WL_CONNECTED){
    digitalWrite(led, HIGH);
    }

  // Vizualização no Monitor Serial!
  if(CONTADOR_LITROS == 1){
    Serial.println("PULSOS: " + String(CONTADOR_PULSOS) + " PULSOS");
    Serial.print("LITROS: ");
    Serial.print(CONTADOR_LITROS);
    Serial.println();
    delay(1000);
   }
   else if(CONTADOR_PULSOS == 1){
    Serial.println("PULSOS: " + String(CONTADOR_PULSOS) + " PULSO");
    Serial.print("LITROS: ");
    Serial.print(CONTADOR_LITROS);
    Serial.println();
    delay(1000);
   }
   else if(CONTADOR_LITROS == VALOR_MAXIMO_LITROS){ // Retirar do código quando não for mais necessário Serial.
    Serial.println("O número máximo da contagem de litros foi atingido!");
    Serial.println("A contagem de litros será reiniciada.....");
    delay(1000);
    }
   else{
    Serial.println("PULSOS: " + String(CONTADOR_PULSOS) + " PULSOS");
    Serial.print("LITROS: ");
    Serial.print(CONTADOR_LITROS);
    Serial.println();
    delay(1000);
    }
   
   //Salvando cada litro na EEPROM, A CADA 450 PULSOS! Para entrar na condição, deve-se ver que o valor de litros antigo é diferente do NOVO valor!
    Serial.print("CONTADOR_LITROS: ");
    Serial.println(CONTADOR_LITROS);
    Serial.print("QUANTIDADE_LITROS_ANTIGA: ");
    Serial.println(QUANTIDADE_LITROS_ANTIGA);
    
   if(QUANTIDADE_LITROS_ANTIGA != CONTADOR_LITROS){
    QUANTIDADE_LITROS_ANTIGA = CONTADOR_LITROS;
    EEPROM.put(1, QUANTIDADE_LITROS_ANTIGA);
    EEPROM.commit();
    
    // CAMINHO É A ROTA DEFINIDA DO ENDEREÇO A SER SALVA NO FIREBASE
    if(Firebase.ready() && signupOK){
      if(Firebase.RTDB.setInt(&fbdo, CAMINHO, CONTADOR_LITROS)){
        Serial.println("PASSED");
        Serial.println("PATH: " + fbdo.dataPath());
        Serial.println("TYPE: " + fbdo.dataType());
        }
      else{
        Serial.println("FAILED");
        Serial.println("REASON: " + fbdo.errorReason());
      }
     }    
    }
}
//Função que cácula o número de pulsos e o número de litros
void PULSOS(){
  noInterrupts();
  CONTADOR_PULSOS++;
    if(CONTADOR_PULSOS == 450){
        if(CONTADOR_LITROS == VALOR_MAXIMO_LITROS){ //VALOR_MAXIMO_LITROS vai até 18.446.744.073.709.551.615
          CONTADOR_LITROS = 0 ;
         }
        CONTADOR_LITROS++;
        CONTADOR_PULSOS = 0;
    }
    interrupts();
  }

  
