import os
import commands
import yaml
import string, random

#test_dir = '/root/rally/use_rally/performance_test/glance/'
output_dir = '/var/www/html/rally_report/performance/'
#glance_test_file = test_dir + 'create-and-list-image.yaml'
images_dir = '/home/images/'
#images = ['fedora-20-i386.img', 'fedora-20-x86_64.img',
#          'fedora-21-i386.img', 'fedora-21-x86_64.img',
#          'centos-6.5-x86_64.img', 'centos-7.0-x86_64.img',
#          'ubuntu-10.04-i386.img', 'ubuntu-10.04-x86_64.img',
#          'ubuntu-12.04-i386.img', 'ubuntu-12.04-x86_64.img',
#          'ubuntu-14.04-i386.img', 'ubuntu-14.04-x86_64-raw',
#          'rhel-6.5-x86_64.img', 'rhel-6.6-x86_64.img',
#          'rhel-7.0-x86_64.img', 'rhel-7.1-x86_64.img']


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


def replace_args_and_execute(test_file, images):
    test_context = read_file(test_file)
    new_file = '/tmp/glance.yaml'
    os.mknod(new_file)
    print 'new test file was created'
    write_file(new_file, yaml.dump(test_context))
    for image in images:
        image_location = images_dir + image
        test_context['GlanceImages.create_and_list_image'][0]['args']['image_location'] = image_location
        write_file(new_file, yaml.dump(test_context).split('\n', 1)[1])
    print 'new test file was created'
    print new_file
    (stat, out) = commands.getstatusoutput('rally --log-dir /var/log/ --log-file /var/log/rally.log -d task start %s' % new_file)
    if stat != 0:
        print 'Rally test error, please check rally.log'
    else:
        print 'Rally test successfully!\n'
        # get task UUID and output result
        task_uuid = out.split('\n')[-2].split()[-1]
        output_html = output_dir + 'glance_' + random_str() + '.html'
        output_json = output_dir + 'glance_' + random_str() + '.json'
        commands.getstatusoutput('rally task report %s --out %s' % (task_uuid, output_html))
        commands.getstatusoutput('rally task results %s >> %s' % (task_uuid, output_json))
    os.remove(new_file)


#replace_args_and_execute(glance_test_file, images)
