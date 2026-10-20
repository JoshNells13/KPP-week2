from setuptools import find_packages, setup

package_name = 'rally_miru'

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
  maintainer='nama kelompok',
  maintainer_email='nama@example.com',
  description='Miru, the turtle who races (Python node)',
  license='MIT License',
  tests_require=['pytest'],
  entry_points={
    'console_scripts': [
      'miru = rally_miru.miru_main:main',
    ],
  },
)
