from setuptools import find_packages, setup

package_name = 'radar_tester'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ahmad',
    maintainer_email='a.hamdan@innopolis.university',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'radar_reader = radar_tester.radar_reader:main',
            'pose_fixer = radar_tester.fix_pose:main' 
        ],
    },
)
