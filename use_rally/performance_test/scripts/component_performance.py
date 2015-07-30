import os
import commands
import yaml
import string, random

test_dir = '/root/rally/use_rally/performance_test/'
output_dir = '/var/www/html/rally_report/performance/'
boot_from_image_test_file = test_dir + 'boot.yaml'
boot_from_volume_test_file = test_dir + 'boot-from-volume.yaml'

components = ['nova', 'cinder', 'glance']
sizes = ['10', '50', '100']
flavors = ['m1.small', 'm1.medium', 'm1.large', 'm1.xlarge']
images = ['fedora-20-i386-raw', 'fedora-20-x86_64-raw',
          'fedora-21-i386-raw', 'fedora-21-x86_64-raw',
          'centos-6.5-x86_64-raw', 'centos-7.0-x86_64-raw',
          'ubuntu-10.04-i386-raw', 'ubuntu-10.04-x86_64-raw',
          'ubuntu-12.04-i386-raw', 'ubuntu-12.04-x86_64-raw',
          'ubuntu-14.04-i386-raw', 'ubuntu-14.04-x86_64-raw',
          'rhel-6.5-x86_64-raw', 'rhel-6.6-x86_64-raw',
          'rhel-7.0-x86_64-raw', 'rhel-7.1-x86_64-raw']
image_locations = ['fedora-20-i386.img', 'fedora-20-x86_64.img',
                   'fedora-21-i386.img', 'fedora-21-x86_64.img',
                   'centos-6.5-x86_64.img', 'centos-7.0-x86_64.img',
                   'ubuntu-10.04-i386.img', 'ubuntu-10.04-x86_64.img',
                   'ubuntu-12.04-i386.img', 'ubuntu-12.04-x86_64.img',
                   'ubuntu-14.04-i386.img', 'ubuntu-14.04-x86_64.img',
                   'rhel-6.5-x86_64.img', 'rhel-6.6-x86_64.img',
                   'rhel-7.0-x86_64.img', 'rhel-7.1-x86_64.img']


def read_file(filename):
    """Read the yaml file"""
    try:
        with open(filename, 'r') as f:
            lines_dict = yaml.load(f)
            return lines_dict
    except Exception as e:
        print 'file does not exist'


def write_file(filename, context):
    """Write change back to file"""
    try:
        with open(filename, 'a') as f:
            f.write('%s' % context)
        print 'write to file successfully!\n'
    except Exception as e:
        print 'write to file error'


def random_str(randomlength=8):
    """random file name"""
    letters = list(string.ascii_letters)
    random.shuffle(letters)
    return ''.join(letters[:randomlength])

# TODO
def replace_args(test_context, test_types=None, flavors=None, images=None):
    if images:
        if flavors:
            for flavor in flavors:
                test_context[context.keys()[0])['args']['flavor']['name'] = flavor
                if test_type == 'image':
                    for image in images:
                        test_context[context.keys()[0]][0]['args']['image']['name'] = image
                        write_file(new_file, yaml.dump(test_context))
        else:
            for image in images:
                # TODO
                pass
    if flavors:
        for flavor in flavors:
            test_context[context.keys()[0]][0]['args']['flavor']['name'] = flavor
            test_context[context.keys()[0]][1]['args']['flavor']['name'] = flavor
            for image in images:
                test_context[context.keys()[0]][0]['args']['image']['name'] = image
                test_context[context.keys()[0]][1]['args']['image']['name'] = image
                write_file(new_file, yaml.dump(test_context))
    # TODO
    if test_types:
        pass
    print 'new test file was created'
#   (stat, out) = commands.getstatusoutput('rally -d task start %s' % new_file)
#   if stat != 0:
#       print 'Rally test error, please check rally.log'
#   else:
#       print 'Rally test successfully!\n'
#       # get task UUID and output result
#       task_uuid = out.split('\n')[-2].split()[-1]
#       output_html = output_dir + 'nova_boot-from-' + boot_type + '_' + random_str() + '.html'
#       output_json = output_dir + 'nova_boot-from-' + boot_type + '_' + random_str() + '.json'
#       commands.getstatusoutput('rally task report %s --out %s' % (task_uuid, output_html))
#       commands.getstatusoutput('rally task results %s >> %s' % (task_uuid, output_json))
#   os.remove(new_file)


replace_args_and_execute('image', boot_from_image_test_file, flavors, images)
replace_args_and_execute('volume', boot_from_volume_test_file, flavors, images)
