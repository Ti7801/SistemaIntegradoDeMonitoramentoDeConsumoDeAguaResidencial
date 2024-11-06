
```
> 🌐 Projeto TCC: Sistema Integrado de Monitoramento de Consumo de Água 🌐  

> 📅 Ano de Conclusão: 2023

> 👨‍💻 Desenvolvido por: Tiago Daltro Duarte

```

### 📖 **Sobre o Projeto**

Este projeto propõe uma solução inovadora para o **monitoramento de consumo de água residencial**. Com um dispositivo medidor e uma aplicação web integrados, o sistema permite que consumidores e concessionárias acompanhem dados de uso de água em tempo real, oferecendo uma visão precisa do consumo e automatizando a geração de faturas.

### 🚀 **Funcionalidades Principais**

- **Monitoramento de Consumo em Tempo Real**: 
  - Utilizando um **sensor de vazão YF-S201** e um **microcontrolador ESP32** com conectividade Wi-Fi 📶, o dispositivo mede continuamente o fluxo de água.
  - Os dados são transmitidos diretamente para o **Firebase** ☁️, onde ficam armazenados para consulta imediata pela aplicação web.

- **Aplicação Web de Gestão e Análise**:
  - Desenvolvida em **Python com o framework Django** 🐍, a aplicação web permite que os usuários da concessionárias acessem seu de consumo de água detalhado, incluindo o volume de água utilizado em cada residência.
  - A interface também permite visualizar **dados pessoais dos clientes** e **valor da fatura** de acordo com o consumo mensal.

- **Geração de Faturas Automática** 💳:
  - A partir dos dados coletados, o sistema calcula o valor a ser pago mensalmente com base no consumo registrado, proporcionando precisão e transparência na cobrança.

### 🔧 **Tecnologias e Ferramentas Utilizadas**

- **Dispositivo Medidor**:
  - **ESP32**: Microcontrolador com conectividade Wi-Fi para transmissão dos dados.
  - **Sensor YF-S201**: Responsável pela medição do fluxo de água 💦.
  
- **Back-end e Banco de Dados**:
  - **Firebase** ☁️: Armazenamento em tempo real para os dados de consumo de água.
  - **Python** e **Django** 🐍: Linguagem de programação e framework usados para desenvolvimento da aplicação web.

- **Hospedagem**:
  - **Amazon Web Services (AWS)** 🌐: A aplicação foi implementada na infraestrutura de computação em nuvem da AWS, garantindo escalabilidade e segurança.

### 🧪 **Processo de Testes**

Para validar a eficácia do sistema, o dispositivo foi instalado em um fluxo de água simulado, e as leituras foram monitoradas via aplicação web. Os dados de consumo foram atualizados em tempo real, e as faturas foram geradas automaticamente, confirmando a precisão e funcionalidade do sistema.

### 📊 **Resultados Obtidos**

- 📈 **Monitoramento Eficiente**: O dispositivo é capaz de registrar o consumo de água e enviar as informações à nuvem sem interrupções, oferecendo dados confiáveis.
- 📝 **Gestão Simplificada**: A aplicação web facilita a administração dos dados dos clientes e o cálculo de faturas, permitindo que concessionárias e consumidores acompanhem o uso de forma prática.
- 💡 **Conclusão**: O sistema desenvolvido se mostrou uma solução eficaz e prática para o monitoramento remoto do consumo de água, simplificando a gestão para concessionárias e promovendo o consumo consciente.

---

### 📂 **Estrutura do Repositório**

- [Device_code](https://github.com/Ti7801/SistemaIntegradoDeMonitoramentoDeConsumoDeAguaResidencial/tree/609e9c8fb474c2060b7c2885de116026bfcf6d58/CODIGO_PROTOTIPO_DE_MEDICAO/MONITORAMENTO_SENSOR_INTELIGENTE) 📟: Código e configurações para o ESP32 e o sensor de vazão YF-S201.
- [Aplicação Web](https://github.com/Ti7801/SistemaIntegradoDeMonitoramentoDeConsumoDeAguaResidencial/tree/609e9c8fb474c2060b7c2885de116026bfcf6d58/APLICACAO_WEB) 🌐: Código da aplicação web desenvolvida em Django.
- [Docs](https://repositorio.ifpb.edu.br/jspui/bitstream/177683/2926/1/Tiago%20Daltro%20Duarte%20-%20Sistema%20integrado%20de%20monitoramento%20de%20consumo%20de%20%C3%A1gua%20residencial%20-%20Copia.pdf) 📑: Documentação do projeto, incluindo especificações técnicas e relatórios de teste.

---

### 📞 **Contato**

Caso tenha interesse em saber mais sobre o projeto ou colaborar de alguma forma, fique à vontade para entrar em contato! 🚀

**E-mail**: [tiagodaltro19@gmail.com]  
**LinkedIn**: [https://www.linkedin.com/in/tiago-daltro-35241622a/]

---

