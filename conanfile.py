from conans import ConanFile,tools,AutoToolsBuildEnvironment,MSBuild
import os
import platform
import shutil
from conanos.build import config_scheme


class GnutlsConan(ConanFile):
    name = "gnutls"
    version = "3.5.19"
    subversion = "2"
    description = "GnuTLS is a secure communications library implementing the SSL, TLS and DTLS protocols and technologies around them"
    url = "https://github.com/conanos/gnutls"
    homepage = "https://www.gnutls.org/"
    license = "LGPL-2+"
    patch = "msvc-zlib-libname.patch"
    exports = ["LICENSE", patch]
    generators = "visual_studio", "gcc"
    settings = "os", "compiler", "build_type", "arch"
    options = { "shared": [True, False], "fPIC": [True, False] }
    default_options = { 'shared': True, 'fPIC': True }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        config_scheme(self)

    def requirements(self):
        self.requires.add("zlib/1.2.11@conanos/stable")
        self.requires.add("nettle/3.4.1@conanos/stable")
        self.requires.add("gmp/6.1.2-5@conanos/stable")

    def build_requirements(self):
        self.build_requires("glib/2.58.1@conanos/stable")

    def source(self):
        url_ = "https://github.com/ShiftMediaProject/gnutls/archive/gnutls_{version}.tar.gz"
        version_ = (self.version+"-"+self.subversion).replace('.','_')
        tools.get(url_.format(version=version_))
        if self.settings.os == "Windows":
            tools.patch(patch_file=self.patch)
        extracted_dir = self.name + "-" + "gnutls_%s"%(version_)
        os.rename(extracted_dir, self._source_subfolder)
        #maj_ver = '.'.join(self.version.split('.')[0:2])
        #tarball_name = '{name}-{version}.tar'.format(name=self.name, version=self.version)
        #archive_name = '%s.xz' % tarball_name
        #url_ = 'https://www.gnupg.org/ftp/gcrypt/{0}/v{1}/{2}'.format(self.name, maj_ver, archive_name)
        #tools.download(url_, archive_name)
        #
        #if self.settings.os == 'Windows':
        #    self.run('7z x %s' % archive_name)
        #    self.run('7z x %s' % tarball_name)
        #    os.unlink(tarball_name)
        #else:
        #    self.run('tar -xJf %s' % archive_name)
        #os.rename('%s-%s' %( self.name, self.version), self._source_folder)
        #os.unlink(archive_name)

    def build(self):
        if self.settings.os == "Windows":
            with tools.chdir(os.path.join(self._source_subfolder,"SMP")):
                msbuild = MSBuild(self)
                build_type = str(self.settings.build_type) + ("DLL" if self.options.shared else "")
                msbuild.build("libgnutls.sln",upgrade_project=True, build_type=build_type)
        #pkgconfig_adaption(self,_abspath(self._pkgconfig_folder))
        
        #if self.is_msvc:
        #    self.msvc_build()
        #else:
        #    #self.gcc_build()
        #    self.autotool_build()

    #def msvc_build(self):

    #    cmake = CMake(self)
    #    cmake.configure(build_folder=self._build_folder,
    #      source_folder='.',
    #      defs={'USE_CONAN_IO':True,
    #        'PROJECT_HOME_DIR':_abspath(self._source_folder),            
    #        'ENABLE_TESTS': self.run_checks
    #    })
    #    cmake.build()
    #    if self.run_checks:
    #        cmake.test()
    #    cmake.install()

    #def autotool_build(self):
    #    pkg_config_paths=[_abspath(self._pkgconfig_folder)]
    #    with tools.chdir(self._source_folder):
    #        #self.run('autoreconf')
    #        env_build = AutoToolsBuildEnvironment(self)
    #        _args = ["--enable-introspection", "--enable-local-libopts", "--disable-guile", 
    #                 "--disable-openssl-compatibility","--without-p11-kit", "--enable-zlib", 
    #                 "--disable-doc", "--disable-tests", "--with-included-unistring",
    #                 "--disable-tools"]
    #        
    #        if self.options.shared:
    #            _args.extend(['--enable-shared=yes','--enable-static=no'])
    #        else:
    #            _args.extend(['--enable-shared=no','--enable-static=yes'])

    #        env_build.configure(args=_args, pkg_config_paths=pkg_config_paths)
    #        env_build.make()
    #        env_build.install()

    #def gcc_build(self):
    #    with tools.chdir(self._source_folder):
    #        with tools.environment_append({
    #            'PKG_CONFIG_PATH':'%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig'
    #            %(self.deps_cpp_info["zlib"].rootpath,self.deps_cpp_info["nettle"].rootpath,
    #            self.deps_cpp_info["libtasn1"].rootpath),
    #            'LIBRARY_PATH' : "%s/lib"%(self.deps_cpp_info["gmp"].rootpath),
    #            'C_INCLUDE_PATH' : "%s/include:%s/include"%(self.deps_cpp_info["gmp"].rootpath,self.deps_cpp_info["libtasn1"].rootpath)
    #            }):

    #            _args = ["--prefix=%s/builddir"%(os.getcwd()), '--libdir=%s/builddir/lib'%(os.getcwd()) ,
    #                     "--enable-introspection", "--enable-local-libopts", "--disable-guile", "--disable-openssl-compatibility",
    #                     "--without-p11-kit", "--enable-zlib", "--disable-doc", "--disable-tests", "--with-included-unistring"]

    #            if self.options.shared:
    #                _args.extend(['--enable-shared=yes','--enable-static=no'])
    #            else:
    #                _args.extend(['--enable-shared=no','--enable-static=yes'])
    #            
    #            self.run('./configure %s'%(' '.join(_args)))#space
    #            self.run('make -j4')
    #            self.run('make install')

    def package(self):
        if self.settings.os == "Windows":
            platform = {'x86': 'x86','x86_64': 'x64'}
            rplatform = platform.get(str(self.settings.arch))
            self.copy("*", dst=os.path.join(self.package_folder,"include"), src=os.path.join(self.build_folder,"..", "msvc","include"))
            for i in ["lib","bin"]:
                self.copy("*", dst=os.path.join(self.package_folder,i), src=os.path.join(self.build_folder,"..","msvc",i,rplatform))
            self.copy("*", dst=os.path.join(self.package_folder,"licenses"), src=os.path.join(self.build_folder,"..", "msvc","licenses"))

            tools.mkdir(os.path.join(self.package_folder,"lib","pkgconfig"))
            shutil.copyfile(os.path.join(self.build_folder,self._source_subfolder,"lib","gnutls.pc.in"),
                            os.path.join(self.package_folder,"lib","pkgconfig", "gnutls.pc"))
            replacements_pc = {
                "@prefix@"      : self.package_folder,
                "@exec_prefix@" : "${prefix}/bin",
                "@libdir@"      : "${prefix}/lib",
                "@includedir@"  : "${prefix}/include",
                "@VERSION@"     : self.version,
                "@LIBZ_PC@"       : "",
                "@LIBINTL@"       : "",
                "@LIBSOCKET@"     : "-lws2_32",
                "@LIBNSL@"        : "",
                "@LIBPTHREAD@"    : "",
                "@LIB_SELECT@"    : "-lws2_32",
                "@TSS_LIBS@"      : "-lCrypt32",
                "@GMP_LIBS@"      : "",
                "@LIBUNISTRING@"  : "",
                "@LIBIDN2_LIBS@"  : "",
                "@GNUTLS_REQUIRES_PRIVATE@" : "Requires.private: nettle, hogweed, zlib",
                "-lgnutls" : "-lgnutls -lintl"
            }
            if self.options.shared:
                replacements_pc.update({
                    "-lgnutls" : "-lgnutlsd -lintl"
                })
            for s, r in replacements_pc.items():
                tools.replace_in_file(os.path.join(self.package_folder,"lib","pkgconfig", "gnutls.pc"),s,r)
        #if tools.os_info.is_linux:
        #    with tools.chdir(self._source_folder):
        #        self.copy("*", src="%s/builddir"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        #if self.is_msvc:
        #    self.cpp_info.libs.append("Crypt32")
        #    self.cpp_info.libs.append("ws2_32")
