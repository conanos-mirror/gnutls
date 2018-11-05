from conans import ConanFile, CMake, tools
import os


class GnutlsConan(ConanFile):
    name = "gnutls"
    version = "3.5.18"
    description = "GnuTLS is a secure communications library implementing the SSL, TLS and DTLS protocols and technologies around them"
    url = "https://github.com/conanos/gnutls"
    homepage = "https://www.gnutls.org/"
    license = "LGPLv2Plus"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    requires = "zlib/1.2.11@conanos/dev", "nettle/3.4@conanos/dev", "libtasn1/4.13@conanos/dev", "gmp/6.1.2@conanos/dev"

    source_subfolder = "source_subfolder"

    def source(self):
        maj_ver = '.'.join(self.version.split('.')[0:2])
        tarball_name = '{name}-{version}.tar'.format(name=self.name, version=self.version)
        archive_name = '%s.xz' % tarball_name
        url_ = 'https://www.gnupg.org/ftp/gcrypt/{0}/v{1}/{2}'.format(self.name, maj_ver, archive_name)
        tools.download(url_, archive_name)
        
        if self.settings.os == 'Windows':
            self.run('7z x %s' % archive_name)
            self.run('7z x %s' % tarball_name)
            os.unlink(tarball_name)
        else:
            self.run('tar -xJf %s' % archive_name)
        os.rename('%s-%s' %( self.name, self.version), self.source_subfolder)
        os.unlink(archive_name)

    def build(self):
        with tools.chdir(self.source_subfolder):
            with tools.environment_append({
                'PKG_CONFIG_PATH':'%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig'
                %(self.deps_cpp_info["zlib"].rootpath,self.deps_cpp_info["nettle"].rootpath,
                self.deps_cpp_info["libtasn1"].rootpath),
                'LIBRARY_PATH' : "%s/lib"%(self.deps_cpp_info["gmp"].rootpath),
                'C_INCLUDE_PATH' : "%s/include:%s/include"%(self.deps_cpp_info["gmp"].rootpath,self.deps_cpp_info["libtasn1"].rootpath)
                }):

                _args = ["--prefix=%s/builddir"%(os.getcwd()), '--libdir=%s/builddir/lib'%(os.getcwd()) ,
                         "--enable-introspection", "--enable-local-libopts", "--disable-guile", "--disable-openssl-compatibility",
                         "--without-p11-kit", "--enable-zlib", "--disable-doc", "--disable-tests", "--with-included-unistring"]

                if self.options.shared:
                    _args.extend(['--enable-shared=yes','--enable-static=no'])
                else:
                    _args.extend(['--enable-shared=no','--enable-static=yes'])
                
                self.run('./configure %s'%(' '.join(_args)))#space
                self.run('make -j4')
                self.run('make install')

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)