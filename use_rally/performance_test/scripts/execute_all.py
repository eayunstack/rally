import nova_performance as nova
import glance_performance as glance
import cinder_performance as cinder


test_dir = '/root/rally/use_rally/performance_test/'
output_dir = '/var/www/html/rally_report/performance/'
nova_boot_from_image_test_file = test_dir + 'nova/boot.yaml'
nova_boot_from_volume_test_file = test_dir + 'nova/boot-from-volume.yaml'
cinder_empty_volume_test_file = test_dir + 'cinder/create-empty.yaml'
cinder_from_image_test_file = test_dir + 'cinder/create-from-image.yaml'
cinder_from_volume_test_file = test_dir + 'cinder/create-from-volume.yaml'
glance_test_file = test_dir + 'glance/create-and-list-image.yaml'
flavors = ['m1.small', 'm1.medium', 'm1.large', 'm1.xlarge']
images = ['fedora-20-i386-raw', 'fedora-20-x86_64-raw',
          'fedora-21-i386-raw', 'fedora-21-x86_64-raw',
          'centos-6.5-x86_64-raw', 'centos-7.0-x86_64-raw',
          'ubuntu-10.04-i386-raw', 'ubuntu-10.04-x86_64-raw',
          'ubuntu-12.04-i386-raw', 'ubuntu-12.04-x86_64-raw',
          'ubuntu-14.04-i386-raw', 'ubuntu-14.04-x86_64-raw',
          'rhel-6.5-x86_64-raw', 'rhel-6.6-x86_64-raw',
          'rhel-7.0-x86_64-raw', 'rhel-7.1-x86_64-raw']
image_locations = ['fedora-20-i386-raw.img', 'fedora-20-x86_64-raw.img',
                    'fedora-21-i386-raw.img', 'fedora-21-x86_64-raw.img',
                    'centos-6.5-x86_64-raw.img', 'centos-7.0-x86_64-raw.img',
                    'ubuntu-10.04-i386-raw.img', 'ubuntu-10.04-x86_64-raw.img',
                    'ubuntu-12.04-i386-raw.img', 'ubuntu-12.04-x86_64-raw.img',
                    'ubuntu-14.04-i386-raw.img', 'ubuntu-14.04-x86_64-raw.img',
                    'rhel-6.5-x86_64-raw.img', 'rhel-6.6-x86_64-raw.img',
                    'rhel-7.0-x86_64-raw.img', 'rhel-7.1-x86_64-raw.img']



#nova.replace_args_and_execute('image', nova_boot_from_image_test_file, flavors, images)
#nova.replace_args_and_execute('volume', nova_boot_from_volume_test_file, flavors, images)

#cinder.replace_args_and_execute(cinder_empty_volume_test_file, create_type='empty')
#cinder.replace_args_and_execute(cinder_from_image_test_file, create_type='image', images=images)

glance.replace_args_and_execute(glance_test_file, image_locations)
