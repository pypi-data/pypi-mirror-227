from setuptools import setup, find_packages

setup(
    name='llmx_zk',
    version='0.1.0',
    description='Added azure GPT to the original foundation',
    packages=find_packages(),
    keywords=['python', 'linux', 'llm', 'windows'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
    ],
    install_requires=[
        # 列出项目依赖的其他 Python 包
        'requests',
        'openai',
		'google_auth', 
    ]
)
