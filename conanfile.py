from conans import ConanFile, CMake, tools
import os
import platform
from conanos.build import config_scheme,pkgconfig_adaption


def _abspath(folder):
    return os.path.abspath(folder).replace('\\','/')

class GnutlsConan(ConanFile):
    name = "gnutls"
    version = "3.5.19"
    description = "GnuTLS is a secure communications library implementing the SSL, TLS and DTLS protocols and technologies around them"
    url = "https://github.com/conanos/gnutls"
    homepage = "https://www.gnutls.org/"
    license = "LGPLv2Plus"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    exports_sources = ['CMakeLists.txt','cmake/*']

    requires = "zlib/1.2.11@conanos/stable", "nettle/3.4@conanos/stable", "libtasn1/4.13@conanos/stable", "gmp/6.1.2@conanos/stable"

    _source_folder    ='_source'
    _pkgconfig_folder ='_pkgconfig'
    _build_folder     ='_build'

    @property
    def is_msvc(self):
        return self.settings.compiler == 'Visual Studio'

    @property
    def run_checks(self):
        CONANOS_RUN_CHECKS = os.environ.get('CONANOS_RUN_CHECKS')
        if CONANOS_RUN_CHECKS:
            return self.name in CONANOS_RUN_CHECKS.split()
        return False
		
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
        os.rename('%s-%s' %( self.name, self.version), self._source_folder)
        os.unlink(archive_name)

    def configure(self):
        del self.settings.compiler.libcxx	
        if self.is_msvc:
            del self.options.fPIC
            if self.options.shared:
               raise tools.ConanException("The gnutls package cannot be built shared on Visual Studio.")

    def requirements(self):
        config_scheme(self)

    def build_requirements(self):
        if platform.system() == "Windows":
            self.build_requires("7z_installer/1.0@conan/stable")

    def build(self):
        pkgconfig_adaption(self,_abspath(self._source_folder))
        
        if self.is_msvc:
            self.msvc_build()
        else:
            self.gcc_build()

    def msvc_build(self):

        cmake = CMake(self)
        cmake.configure(build_folder=self._build_folder,
          source_folder='.',
          defs={'USE_CONAN_IO':True,
            'PROJECT_HOME_DIR':_abspath(self._source_folder),            
            'ENABLE_TESTS': self.run_checks
        })
        cmake.build()
        if self.run_checks:
            cmake.test()
        cmake.install()

    def gcc_build(self):
        with tools.chdir(self._source_folder):
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
            with tools.chdir(self._source_folder):
                self.copy("*", src="%s/builddir"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.is_msvc:
            self.cpp_info.libs.append("Crypt32")
            self.cpp_info.libs.append("ws2_32")
