AIOWatcher
==========

.. image:: https://i.pinimg.com/originals/1b/2a/2a/1b2a2a3a94cae52f318e1893303a0834.png
   :height: 126px
   :width: 256px
   :alt: aiowatcher logo

|

.. image:: https://img.shields.io/github/repo-size/py-paulo/aiowatcher 
    :target: https://img.shields.io/github/repo-size/py-paulo/aiowatcher
    :alt: GitHub repo size

.. image:: https://img.shields.io/pypi/v/AIOWatcher
    :target: https://img.shields.io/pypi/v/aiowatcher
    :alt: PyPI

.. image:: https://img.shields.io/pypi/wheel/aiowatcher
    :target: https://img.shields.io/pypi/wheel/aiowatcher
    :alt: PyPI - Wheel

.. image:: https://img.shields.io/github/license/py-paulo/aiowatcher   
    :target: https://img.shields.io/github/license/py-paulo/aiowatcher
    :alt: GitHub

.. image:: https://img.shields.io/github/last-commit/py-paulo/aiowatcher
    :target: https://img.shields.io/github/last-commit/py-paulo/aiowatcher
    :alt: GitHub last commit

Biblioteca para "observar" os arquivos de um diretório e chamar uma 
função de callback `(filename, lines)` toda vez que um dos arquivos monitorados for gravado, em tempo real.

Em termos práticos, isso pode ser comparado ao comando `tail -F * .log` do UNIX, 
mas em vez de ter linhas impressas no stdout, uma função Python é chamada.

Da mesma forma que o tail, ele se encarrega de "observar" os novos arquivos que são 
criados após a inicialização e "desbloquear" aqueles que são removidos nesse meio tempo. 
Isso significa que você será capaz de "seguir" e suportar também arquivos de log rotativos.

Key Features
============

- Utiliza Asyncio para leitura e monitoramento assincrono.
- A implementação escolhe automaticamente dependendo da compatibilidade do sistema.
- Monitoramento de diversos arquivos em um mesmo diretório ou apenas de um.
- Função `callback` assincrona.

Getting started
---------------

Todos os exemplos de código requerem Python 3.6+.

Basic Usage
+++++++++++

.. code-block:: python

    import asyncio
    from aiowatcher import AIOWatcher

    async def callback(filename, line):
        print(line)

    async def main():
        lw = AIOWatcher('var', callback, extensions=['txt'])
        await lw.init()
        await lw.loop()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())    


Non blocking
++++++++++++

.. code-block:: python

    import asyncio
    from aiowatcher import AIOWatcher

    async def callback(filename, line):
        print(line)

    async def main():
        lw = AIOWatcher('var', callback, extensions=['txt'])
        while True:
            await lw.loop(blocking=False)
            await asyncio.sleep(0.1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


License
=======

``aiowatcher`` é oferecido sob a licença Apache 2.


Source code
===========

A versão mais recente do desenvolvedor está disponível em um repositório GitHub:
https://github.com/py-paulo/aiowatcher.git
