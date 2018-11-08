from conans import ConanFile, CMake, tools
import os

class Gobjectintrospectionm4Conan(ConanFile):
    name = "gobject-introspection-m4"
    version = "1.58.0"
    description = "GObject introspection is a middleware layer between C libraries (using GObject) and language bindings."
    url = "https://github.com/conan-multimedia/gobject-introspection-m4"
    homepage = "https://wiki.gnome.org/Projects/GObjectIntrospection"
    license = "GPLv2Plus"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    source_subfolder = "source_subfolder"

    def source(self):
        maj_ver = '.'.join(self.version.split('.')[0:2])
        _name = "gobject-introspection"
        tarball_name = '{name}-{version}.tar'.format(name=_name, version=self.version)
        archive_name = '%s.xz' % tarball_name
        url_ = 'http://ftp.gnome.org/pub/GNOME/sources/{0}/{1}/{2}'.format(_name,maj_ver, archive_name)
        tools.download(url_, archive_name)
        
        if self.settings.os == 'Windows':
            self.run('7z x %s' % archive_name)
            self.run('7z x %s' % tarball_name)
            os.unlink(tarball_name)
        else:
            self.run('tar -xJf %s' % archive_name)
        os.rename('%s-%s'%(_name,self.version) , self.source_subfolder)
        os.unlink(archive_name)

    def build(self):
        pass

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("introspection.m4", dst="share/aclocal", src="%s/m4"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

