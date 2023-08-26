from setuptools import setup, find_packages
setup(
        script_name='akksnna/__init__.py',    
        name="akksnna", 
        version='0.0.1',
        author="esfelurm",
        author_email="esfelurm@yahoo.com",
        description='Telegram for Hackers',
        long_description='Hello dear friend who uses our library\nthis module is at your service with speed and security!\n\nWhat is Telegram FHK module?\nIt means "Telegram for hackers".\n\nWhy is this module trusted by hackers?\n\nBecause this module is written with simple codes and has high speed and is safe!\n\nTo read the module document, refer to the channel below : https://t.me/Telfhk\n\nWhat are the features of this module?\n\n- High speed\n- safe\n- Send message without filter for Iranians\n- Download the file from the site through a robot without filters for Iranians\n- Has practical methods\n- Updated every month + new options',
        packages=find_packages('telfhk.py'),
        install_requires=['colorama','requests'], 
        project_urls = {'Documentation':'https://t.me/TelFHk'},
        
        keywords=['..:::Telegram For Hackers:::..'],
        classifiers= [
            "Programming Language :: Python :: 3",
        ]
)