import os, sys, mmap

def ags_fields(ags_file_path):
    ags_file = open(ags_file_path, 'r+b')
    mm = mmap.mmap(ags_file.fileno(), 0)

    previous = None
    cr = False

    key = ""
    key_list = []

    for i in range(len(mm)):
        h = mm[i].encode('hex')

        if h == previous == "00" and not cr:
            #print
            key_list.append(key)
            key = ""
            cr = True
            continue

        d = int(h, 16)

        if d >=  32 and d <= 127:
            c = mm[i].encode('ascii')
            #print c,
            key += c
            cr = False

        previous = h

    #print
    #print key_list
    #print

    user_index = key_list.index('USER')
    user = key_list[user_index + 1]

    password_index = key_list.index('PASSWORD')
    password = key_list[password_index + 3]
    eq_index = password.find('=')
    password = password[2:eq_index].encode('hex')

    resturl_index = key_list.index('RestUrl')
    resturl = key_list[resturl_index + 2]

    tokenurl_index = key_list.index('AdminTokenUrl')
    tokenurl = key_list[tokenurl_index + 2]

    rsaurl_index = key_list.index('RsaUrl')
    rsaurl = key_list[rsaurl_index + 2]

    print "file: %s" % ags_file_path
    print "user: %s" % user
    print "password: %s" % password
    print "rest url: %s" % resturl
    print "rest url: %s" % tokenurl
    print "rest url: %s" % rsaurl
    print

    mm.close()
    ags_file.close()

    return {'USER':user,
            'PASSWORD':password,
            'RestUrl':resturl,
            'AdminTokenUrl':tokenurl_index,
            'RsaUrl':rsaurl}

def all_ags_in_dir(path):
    items = os.listdir(path)
    for item in items:
        try:
            if os.path.splitext(item)[1] == '.ags':
                ags_fields(os.path.join(path, item))
        except:
            print "%s is not an ags connection file" % item

if __name__ == "__main__":
    if len(sys.argv) > 1:
        all_ags_in_dir(sys.argv[1])
    else:
        print "please provide a directory to search"
