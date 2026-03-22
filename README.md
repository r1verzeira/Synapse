# ⚡ Synapse: High-Performance Network Stress Engine

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey?style=for-the-badge&logo=linux)

**Synapse** é um motor de engenharia de rede desenvolvido em Python para testar a resiliência de infraestruturas TCP/IP. Diferente de scripts convencionais, ele foca em performance bruta ao operar diretamente na Camada 3 do modelo OSI, utilizando técnicas avançadas de paralelismo.

---

### 🚀 Diferenciais Técnicos

O sistema foi arquitetado para extrair o máximo do hardware disponível, focando em baixa latência de disparo:

* **Multiprocessing Control:** Ignora o *Global Interpreter Lock* (GIL) do Python, escalando a execução para todos os núcleos da CPU de forma 100% paralela. 🧠
* **Raw Sockets (L3):** Utiliza a flag `IP_HDRINCL` para ignorar a stack TCP/IP padrão do sistema operacional, permitindo a construção manual de cabeçalhos. 🏗️
* **Dynamic IP Spoofing:** Cada pacote gerado possui um endereço de origem aleatório (Randomized Source IP), simulando tráfego distribuído. 🌍
* **Randomized Payloads:** Injeção de ruído binário aleatório para variar o MTU e evitar detecção por assinaturas estáticas de DPI (*Deep Packet Inspection*). 🎲

# ⚖️ Disclaimer (Fins Educativos)

Este software foi desenvolvido exclusivamente para fins educacionais, pesquisa acadêmica e auditorias de segurança autorizadas.

O uso desta ferramenta contra alvos sem permissão expressa e por escrito é **ilegal e antiético**. O autor não se responsabiliza por quaisquer danos ou consequências legais resultantes do uso indevido deste código. Use com responsabilidade em ambientes controlados.
