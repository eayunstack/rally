import os
import commands
import yaml
import string, random

#test_dir = '/root/rally/use_rally/performance_test/cinder/'
output_dir = '/var/www/html/rally_report/performance/'
#empty_volume_test_file = test_dir + 'create-empty.yaml'
#from_image_test_file = test_dir + 'create-from-image.yaml'
#from_volume_test_file = test_dir + 'create-from-volume.yaml'
sizes = ['10', '50', '100']
#images = ['fedora-20-i386-raw', 'fedora-20-x86_64-raw',
#          'fedora-21-i386-raw', 'fedora-21-x86_64-raw',
#          'centos-6.5-x86_64-raw', 'centos-7.0-x86_64-raw',
#          'ubuntu-10.04-i386-raw', 'ubuntu-10.04-x86_64-raw',
#          'ubuntu-12.04-i386-raw', 'ubuntu-12.04-x86_64-raw',
#          'ubuntu-14.04-i386-raw', 'ubuntu-14.04-x86_64-raw',
#          'rhel-6.5-x86_64-raw', 'rhel-6.6-x86_64-raw',
#          'rhel-7.0-x86_64-raw', 'rhel-7.1-x86_64-raw']


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


def replace_args_and_execute(test_file, create_type=None, images=None):
    test_context = read_file(test_file)
    new_file = '/tmp/cinder_from-' + create_type + '.yaml'
    os.mknod(new_file)
    print new_file
    write_file(new_file, yaml.dump(test_context))
    if create_type == 'empty':
        for size in sizes:
            test_context['CinderVolumes.create_volume'][0]['args']['size'] = size
            test_context['CinderVolumes.create_volume'][1]['args']['size'] = size
            write_file(new_file, yaml.dump(test_context).split('\n', 1)[1])
    if create_type == 'image' and images != None:
        for size in sizes:
            test_context['CinderVolumes.create_and_delete_volume'][0]['args']['size'] = size
            test_context['CinderVolumes.create_and_delete_volume'][1]['args']['size'] = size
            for image in images:
                test_context['CinderVolumes.create_and_delete_volume'][0]['args']['image']['name'] = image
                test_context['CinderVolumes.create_and_delete_volume'][1]['args']['image']['name'] = image
                #write_file(new_file, yaml.dump(test_context).split('\n', 1)[1])
                write_file(new_file, yaml.dump(test_context['CinderVolumes.create_and_delete_volume'][1:]))
    # TODO
#    if create_type == 'volume':
#        for size in sizes:
#            test_context['CinderVolumes.create_volume'][0]['args']['size'] = size
#            test_context['CinderVolumes.create_volume'][1]['args']['size'] = size
    print 'new test file was created'
    print new_file
    (stat, out) = commands.getstatusoutput('rally --log-dir /var/log/ --log-file /var/log/rally.log -d task start %s' % new_file)
    if stat != 0:
        print 'Rally test error, please check rally.log'
    else:
        print 'Rally test successfully!\n'
        # get task UUID and output result
        task_uuid = out.split('\n')[-2].split()[-1]
        output_html = output_dir + 'cinder_from-' + create_type + '_' + random_str() + '.html'
        output_json = output_dir + 'cinder_from-' + create_type + '_' + random_str() + '.json'
        commands.getstatusoutput('rally task report %s --out %s' % (task_uuid, output_html))
        commands.getstatusoutput('rally task results %s >> %s' % (task_uuid, output_json))
    os.remove(new_file)


#replace_args_and_execute(empty_volume_test_file, create_type='empty')
#replace_args_and_execute(from_image_test_file, create_type='image', images=images)
