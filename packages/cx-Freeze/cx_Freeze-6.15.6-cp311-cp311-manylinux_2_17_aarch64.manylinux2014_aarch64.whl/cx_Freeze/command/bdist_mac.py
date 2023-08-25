"""Extends setuptools to build macOS dmg or app blundle."""

from __future__ import annotations

import os
import plistlib
import shutil
import subprocess

from setuptools import Command

from cx_Freeze.common import normalize_to_list
from cx_Freeze.darwintools import (
    DarwinFile,
    DarwinFileTracker,
    applyAdHocSignature,
    changeLoadReference,
)

from ..exception import OptionError

__all__ = ["BdistDMG", "BdistMac"]


class BdistDMG(Command):
    """Create a Mac DMG disk image containing the Mac application bundle."""

    description = (
        "create a Mac DMG disk image containing the Mac application bundle"
    )
    user_options = [
        ("volume-label=", None, "Volume label of the DMG disk image"),
        (
            "applications-shortcut=",
            None,
            "Boolean for whether to include "
            "shortcut to Applications in the DMG disk image",
        ),
        ("silent", "s", "suppress all output except warnings"),
    ]

    def initialize_options(self):
        self.volume_label = self.distribution.get_fullname()
        self.applications_shortcut = False
        self.silent = None

    def finalize_options(self):
        if self.silent is None:
            self.silent = False

    def build_dmg(self):
        # Remove DMG if it already exists
        if os.path.exists(self.dmg_name):
            os.unlink(self.dmg_name)

        # Make dist folder
        self.dist_dir = os.path.join(self.build_dir, "dist")
        if os.path.exists(self.dist_dir):
            shutil.rmtree(self.dist_dir)
        self.mkpath(self.dist_dir)

        # Copy App Bundle
        dest_dir = os.path.join(
            self.dist_dir, os.path.basename(self.bundle_dir)
        )
        self.copy_tree(self.bundle_dir, dest_dir)

        createargs = [
            "hdiutil",
            "create",
        ]
        if self.silent:
            createargs += ["-quiet"]
        createargs += [
            "-fs",
            "HFSX",
            "-format",
            "UDZO",
            self.dmg_name,
            "-imagekey",
            "zlib-level=9",
            "-srcfolder",
            self.dist_dir,
            "-volname",
            self.volume_label,
        ]

        if self.applications_shortcut:
            apps_folder_link = os.path.join(self.dist_dir, "Applications")
            os.symlink(
                "/Applications", apps_folder_link, target_is_directory=True
            )

        # Create the dmg
        if subprocess.call(createargs) != 0:
            raise OSError("creation of the dmg failed")

    def run(self):
        # Create the application bundle
        self.run_command("bdist_mac")

        # Find the location of the application bundle and the build dir
        self.bundle_dir = self.get_finalized_command("bdist_mac").bundle_dir
        self.build_dir = self.get_finalized_command("build_exe").build_base

        # Set the file name of the DMG to be built
        self.dmg_name = os.path.join(
            self.build_dir, self.volume_label + ".dmg"
        )

        self.execute(self.build_dmg, ())


class BdistMac(Command):
    """Create a Mac application bundle."""

    description = "create a Mac application bundle"

    plist_items: list[tuple[str, str]]
    include_frameworks: list[str]
    include_resources: list[str]

    user_options = [
        ("iconfile=", None, "Path to an icns icon file for the application."),
        (
            "qt-menu-nib=",
            None,
            "Location of qt_menu.nib folder for Qt "
            "applications. Will be auto-detected by default.",
        ),
        (
            "bundle-name=",
            None,
            "File name for the bundle application "
            "without the .app extension.",
        ),
        (
            "plist-items=",
            None,
            "A list of key-value pairs (type: List[Tuple[str, str]]) to "
            "be added to the app bundle Info.plist file.",
        ),
        (
            "custom-info-plist=",
            None,
            "File to be used as the Info.plist in "
            "the app bundle. A basic one will be generated by default.",
        ),
        (
            "include-frameworks=",
            None,
            "A comma separated list of Framework "
            "directories to include in the app bundle.",
        ),
        (
            "include-resources=",
            None,
            "A list of tuples of additional "
            "files to include in the app bundle's resources directory, with "
            "the first element being the source, and second the destination "
            "file or directory name.",
        ),
        (
            "codesign-identity=",
            None,
            "The identity of the key to be used to sign the app bundle.",
        ),
        (
            "codesign-entitlements=",
            None,
            "The path to an entitlements file "
            "to use for your application's code signature.",
        ),
        (
            "codesign-deep=",
            None,
            "Boolean for whether to codesign using the --deep option.",
        ),
        (
            "codesign-resource-rules",
            None,
            "Plist file to be passed to "
            "codesign's --resource-rules option.",
        ),
        (
            "absolute-reference-path=",
            None,
            "Path to use for all referenced "
            "libraries instead of @executable_path.",
        ),
    ]

    def initialize_options(self):
        self.list_options = [
            "plist_items",
            "include_frameworks",
            "include_resources",
        ]
        for option in self.list_options:
            setattr(self, option, [])

        self.absolute_reference_path = None
        self.bundle_name = self.distribution.get_fullname()
        self.codesign_deep = None
        self.codesign_entitlements = None
        self.codesign_identity = None
        self.codesign_resource_rules = None
        self.custom_info_plist = None
        self.iconfile = None
        self.qt_menu_nib = False

    def finalize_options(self):
        # Make sure all options of multiple values are lists
        for option in self.list_options:
            setattr(self, option, normalize_to_list(getattr(self, option)))
        for item in self.plist_items:
            if not isinstance(item, tuple) or len(item) != 2:
                raise OptionError(
                    "Error, plist_items must be a list of key, value pairs "
                    "(List[Tuple[str, str]]) (bad list item)."
                )

    def create_plist(self):
        """Create the Contents/Info.plist file."""
        # Use custom plist if supplied, otherwise create a simple default.
        if self.custom_info_plist:
            with open(self.custom_info_plist, "rb") as file:
                contents = plistlib.load(file)
        else:
            contents = {
                "CFBundleIconFile": "icon.icns",
                "CFBundleDevelopmentRegion": "English",
                "CFBundleIdentifier": self.bundle_name,
                # Specify that bundle is an application bundle
                "CFBundlePackageType": "APPL",
                # Cause application to run in high-resolution mode by default
                # (Without this, applications run from application bundle may
                # be pixelated)
                "NSHighResolutionCapable": "True",
            }

        # Ensure CFBundleExecutable is set correctly
        contents["CFBundleExecutable"] = self.bundle_executable

        # add custom items to the plist file
        for key, value in self.plist_items:
            contents[key] = value

        with open(os.path.join(self.contents_dir, "Info.plist"), "wb") as file:
            plistlib.dump(contents, file)

    def set_absolute_reference_paths(self, path=None):
        """For all files in Contents/MacOS, set their linked library paths to
        be absolute paths using the given path instead of @executable_path.
        """
        if not path:
            path = self.absolute_reference_path

        files = os.listdir(self.bin_dir)

        for filename in files:
            filepath = os.path.join(self.bin_dir, filename)

            # Skip some file types
            if filepath[-1:] in ("txt", "zip") or os.path.isdir(filepath):
                continue

            out = subprocess.check_output(
                ("otool", "-L", filepath), encoding="utf-8"
            )
            for line in out.splitlines()[1:]:
                lib = line.lstrip("\t").split(" (compat")[0]

                if lib.startswith("@executable_path"):
                    replacement = lib.replace("@executable_path", path)

                    path, name = os.path.split(replacement)

                    # see if we provide the referenced file;
                    # if so, change the reference
                    if name in files:
                        subprocess.call(
                            (
                                "install_name_tool",
                                "-change",
                                lib,
                                replacement,
                                filepath,
                            )
                        )
            applyAdHocSignature(filepath)

    def set_relative_reference_paths(self, build_dir: str, bin_dir: str):
        """Make all the references from included Mach-O files to other included
        Mach-O files relative.
        """
        darwin_file: DarwinFile

        for darwin_file in self.darwin_tracker:
            # get the relative path to darwin_file in build directory
            relative_copy_dest = os.path.relpath(
                darwin_file.getBuildPath(), build_dir
            )
            # figure out directory where it will go in binary directory for
            # .app bundle, this would be the Content/MacOS subdirectory in
            # bundle.  This is the file that needs to have its dynamic load
            # references updated.
            file_path_in_bin_dir = os.path.join(bin_dir, relative_copy_dest)

            # for each file that this darwin_file references, update the
            # reference as necessary; if the file is copied into the binary
            # package, change the reference to be relative to @executable_path
            # (so an .app bundle will work wherever it is moved)
            for reference in darwin_file.getMachOReferenceList():
                if not reference.is_copied:
                    # referenced file not copied -- assume this is a system
                    # file that will also be present on the user's machine,
                    # and do not change reference
                    continue
                # this is the reference in the machO file that needs to be
                # updated
                raw_path = reference.raw_path
                ref_target_file: DarwinFile = reference.target_file
                # this is where file copied in build dir
                abs_build_dest = ref_target_file.getBuildPath()
                rel_build_dest = os.path.relpath(abs_build_dest, build_dir)
                exe_path = f"@executable_path/{rel_build_dest}"
                changeLoadReference(
                    file_path_in_bin_dir,
                    oldReference=raw_path,
                    newReference=exe_path,
                    VERBOSE=False,
                )

            applyAdHocSignature(file_path_in_bin_dir)

    def find_qt_menu_nib(self):
        """Returns a location of a qt_menu.nib folder, or None if this is not
        a Qt application.
        """
        if self.qt_menu_nib:
            return self.qt_menu_nib
        if any(n.startswith("PyQt4.QtCore") for n in os.listdir(self.bin_dir)):
            name = "PyQt4"
        elif any(
            n.startswith("PySide.QtCore") for n in os.listdir(self.bin_dir)
        ):
            name = "PySide"
        else:
            return None

        qtcore = __import__(name, fromlist=["QtCore"]).QtCore
        libpath = str(
            qtcore.QLibraryInfo.location(qtcore.QLibraryInfo.LibrariesPath)
        )
        for subpath in [
            "QtGui.framework/Resources/qt_menu.nib",
            "Resources/qt_menu.nib",
        ]:
            path = os.path.join(libpath, subpath)
            if os.path.exists(path):
                return path

        # Last resort: fixed paths (macports)
        for path in [
            "/opt/local/Library/Frameworks/QtGui.framework/Versions/"
            "4/Resources/qt_menu.nib"
        ]:
            if os.path.exists(path):
                return path

        print("Could not find qt_menu.nib")
        raise OSError("Could not find qt_menu.nib")

    def prepare_qt_app(self):
        """Add resource files for a Qt application. Should do nothing if the
        application does not use QtCore.
        """
        nib_locn = self.find_qt_menu_nib()
        if nib_locn is None:
            return

        # Copy qt_menu.nib
        self.copy_tree(
            nib_locn, os.path.join(self.resources_dir, "qt_menu.nib")
        )

        # qt.conf needs to exist, but needn't have any content
        with open(os.path.join(self.resources_dir, "qt.conf"), "wb"):
            pass

    def run(self):
        self.run_command("build_exe")
        build_exe = self.get_finalized_command("build_exe")
        freezer: freezer.Freezer = build_exe.freezer

        # Define the paths within the application bundle
        self.bundle_dir = os.path.join(
            build_exe.build_base, self.bundle_name + ".app"
        )
        self.contents_dir = os.path.join(self.bundle_dir, "Contents")
        self.resources_dir = os.path.join(self.contents_dir, "Resources")
        self.bin_dir = os.path.join(self.contents_dir, "MacOS")
        self.frameworks_dir = os.path.join(self.contents_dir, "Frameworks")

        # Find the executable name
        executable = self.distribution.executables[0].target_name
        _, self.bundle_executable = os.path.split(executable)

        # Build the app directory structure
        self.mkpath(self.resources_dir)
        self.mkpath(self.bin_dir)
        self.mkpath(self.frameworks_dir)

        self.copy_tree(build_exe.build_exe, self.bin_dir)

        # Copy the icon
        if self.iconfile:
            self.copy_file(
                self.iconfile, os.path.join(self.resources_dir, "icon.icns")
            )

        # Copy in Frameworks
        for framework in self.include_frameworks:
            self.copy_tree(
                framework,
                os.path.join(self.frameworks_dir, os.path.basename(framework)),
            )

        # Copy in Resources
        for resource, destination in self.include_resources:
            if os.path.isdir(resource):
                self.copy_tree(
                    resource, os.path.join(self.resources_dir, destination)
                )
            else:
                parent_dirs = os.path.dirname(
                    os.path.join(self.resources_dir, destination)
                )
                os.makedirs(parent_dirs, exist_ok=True)
                self.copy_file(
                    resource, os.path.join(self.resources_dir, destination)
                )

        # Create the Info.plist file
        self.execute(self.create_plist, ())

        # Make all references to libraries relative
        self.darwin_tracker: DarwinFileTracker = freezer.darwin_tracker
        self.execute(
            self.set_relative_reference_paths,
            (
                os.path.abspath(build_exe.build_exe),
                os.path.abspath(self.bin_dir),
            ),
        )

        # Make library references absolute if enabled
        if self.absolute_reference_path:
            self.execute(self.set_absolute_reference_paths, ())

        # For a Qt application, run some tweaks
        self.execute(self.prepare_qt_app, ())

        # Sign the app bundle if a key is specified
        if self.codesign_identity:
            signargs = ["codesign", "-s", self.codesign_identity]

            if self.codesign_entitlements:
                signargs.append("--entitlements")
                signargs.append(self.codesign_entitlements)

            if self.codesign_deep:
                signargs.insert(1, "--deep")

            if self.codesign_resource_rules:
                signargs.insert(
                    1, "--resource-rules=" + self.codesign_resource_rules
                )

            signargs.append(self.bundle_dir)

            if subprocess.call(signargs) != 0:
                raise OSError("Code signing of app bundle failed")
