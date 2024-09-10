 #!/usr/bin/env python
#
# Hi There!
#
# You may be wondering what this giant blob of binary data here is, you might
# even be worried that we're up to something nefarious (good for you for being
# paranoid!). This is a base85 encoding of a zip file, this zip file contains
# an entire copy of pip (version 24.2).
#
# Pip is a thing that installs packages, pip itself is a package that someone
# might want to install, especially if they're looking to run this get-pip.py
# script. Pip has a lot of code to deal with the security of installing
# packages, various edge cases on various platforms, and other such sort of
# "tribal knowledge" that has been encoded in its code base. Because of this
# we basically include an entire copy of pip inside this blob. We do this
# because the alternatives are attempt to implement a "minipip" that probably
# doesn't do things correctly and has weird edge cases, or compress pip itself
# down into a single file.
#
# If you're wondering how this is created, it is generated using
# `scripts/generate.py` in https://github.com/pypa/get-pip.

import sys

this_python = sys.version_info[:2]
min_version = (3, 8)
if this_python < min_version:
    message_parts = [
        "This script does not work on Python {}.{}.".format(*this_python),
        "The minimum supported Python version is {}.{}.".format(*min_version),
        "Please use https://bootstrap.pypa.io/pip/{}.{}/get-pip.py instead.".format(*this_python),
    ]
    print("ERROR: " + " ".join(message_parts))
    sys.exit(1)


import os.path
import pkgutil
import shutil
import tempfile
import argparse
import importlib
from base64 import b85decode


def include_setuptools(args):
    """
    Install setuptools only if absent, not excluded and when using Python <3.12.
    """
    cli = not args.no_setuptools
    env = not os.environ.get("PIP_NO_SETUPTOOLS")
    absent = not importlib.util.find_spec("setuptools")
    python_lt_3_12 = this_python < (3, 12)
    return cli and env and absent and python_lt_3_12


def include_wheel(args):
    """
    Install wheel only if absent, not excluded and when using Python <3.12.
    """
    cli = not args.no_wheel
    env = not os.environ.get("PIP_NO_WHEEL")
    absent = not importlib.util.find_spec("wheel")
    python_lt_3_12 = this_python < (3, 12)
    return cli and env and absent and python_lt_3_12


def determine_pip_install_arguments():
    pre_parser = argparse.ArgumentParser()
    pre_parser.add_argument("--no-setuptools", action="store_true")
    pre_parser.add_argument("--no-wheel", action="store_true")
    pre, args = pre_parser.parse_known_args()

    args.append("pip")

    if include_setuptools(pre):
        args.append("setuptools")

    if include_wheel(pre):
        args.append("wheel")

    return ["install", "--upgrade", "--force-reinstall"] + args


def monkeypatch_for_cert(tmpdir):
    """Patches `pip install` to provide default certificate with the lowest priority.

    This ensures that the bundled certificates are used unless the user specifies a
    custom cert via any of pip's option passing mechanisms (config, env-var, CLI).

    A monkeypatch is the easiest way to achieve this, without messing too much with
    the rest of pip's internals.
    """
    from pip._internal.commands.install import InstallCommand

    # We want to be using the internal certificates.
    cert_path = os.path.join(tmpdir, "cacert.pem")
    with open(cert_path, "wb") as cert:
        cert.write(pkgutil.get_data("pip._vendor.certifi", "cacert.pem"))

    install_parse_args = InstallCommand.parse_args

    def cert_parse_args(self, args):
        if not self.parser.get_default_values().cert:
            # There are no user provided cert -- force use of bundled cert
            self.parser.defaults["cert"] = cert_path  # calculated above
        return install_parse_args(self, args)

    InstallCommand.parse_args = cert_parse_args


def bootstrap(tmpdir):
    monkeypatch_for_cert(tmpdir)

    # Execute the included pip and use it to install the latest pip and
    # any user-requested packages from PyPI.
    from pip._internal.cli.main import main as pip_entry_point
    args = determine_pip_install_arguments()
    sys.exit(pip_entry_point(args))


def main():
    tmpdir = None
    try:
        # Create a temporary working directory
        tmpdir = tempfile.mkdtemp()

        # Unpack the zipfile into the temporary directory
        pip_zip = os.path.join(tmpdir, "pip.zip")
        with open(pip_zip, "wb") as fp:
            fp.write(b85decode(DATA.replace(b"\n", b"")))

        # Add the zipfile to sys.path so that we can import it
        sys.path.insert(0, pip_zip)

        # Run the bootstrap
        bootstrap(tmpdir=tmpdir)
    finally:
        # Clean up our temporary working directory
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)


DATA = b"""
P)h>@6aWAK2mofX{8+Vkj=%N*003hF000jF003}la4%n9X>MtBUtcb8c|B0UYQr!Lz56RfE?c3qp%k_
SHrQn_7~2lJl@i=UNd$>)BxNOkKc^)X0-?v#)8n-qN6<M@=zzu)S>cmJxA2{mV(^18RrQA~d8sORfnv
9}yTTaLU<;$CaPPU3^2R?b=Lb<f9y9wZ2He2ID^SqVK(3-FetQzg?ZW~i=PP*o`G6RP8AkL$p^XfaAe
?4Ml<oxLIY1qQ!~sESrlexcMesdSebdnOJv6AE2HAojLa&;nbgm=qr<1MY=+d0L%bJcvCKUI$e}1y7v
&(FkNHW7#t2;Ysmb4g@=M*z4YgW~neM-nzD~vjExPg~sHs&8tO9KQH000080A{lMSa0{Q*SrA$09FG4
01p5F0B~t=FJE76VQFq(UoLQYT~bSL+b|5i`&SU@!Oq~iIS)&L9d|8u8wNv=>6nNu38Ea&`}HFgyJ@G
B9{e8sD4K$g2|O2c-|@;t@dR%;`5Qu6f^i+#IYx8|79X$VF3?d#n|xfMkA8wQAoLVDffU76;J#O)CYU
tTKs|(rtOUt}xq0efX64y=-}wYe4gv+Rewsv@!47DzwFn{pMIm#X%sAFClIW>99{f@Za2e3a^UYte1H
%y3G<XNkQ|9}&5xy4m@b>HUTlK2Lp_T}m3nsgC)$#bX09kug6MU#nM~&r24-0~c2yu2!TgU+z6-O~;x
-O@YkJ|0dA=sY-F^F})aITrzTyS?O7N5T~%P_vE*{#XPt(tDzVC+>eZ42i!91eGvPx8>ysJFuZiRYzl
Cqu4no3L)R_c2M{&P)haML0zYtRpKw0?HZ~t=E9}0<93*a^reKp2wsiXosq<ZDnF1d&EGAaqKtH_neS
PAHxCm8ml!jzxyu~m0X`+&pMkth|PEP|9MZ~c>Fv#$q{3!PIV@d3Fa6TvSqmUyJeY&DcVg-E}?LbjUB
1cn%!C6%kRp-;$05^P^$8se4pYUP)h>@6aWAK2mofX{8&kI@w?Rm00625000#L003}la4%n9aA|NYa&
>NQWpZC%E^v8$RKZT$KoGtAD+Y6@Eg2U<4^`Aul~7Q*kTeO0ilWuV9+Rc^uGwAFScre`j2$Ns(fW|Ac
W2(bdGpp`7)~~rH68&sGV^5%eytp2rf$I$P^&tDKZ^D=NXS)DphfKg^^>wjSF}!pV96<kDiP>k%L;Rl
4wR?Y1iYbW*H|QE>3jIf<PAk<Qh)HUqO__u)>GP(l7ZCQcW_>M>}!N!7zD@g@#q(H)t=BgWi%13YU$N
VmCCn}tugxz4l~bZRpUDJS?kyIdbSHLF=eD680xf+!7og$h(lpb1$A3n^FTnUH&q$TelEXHuf=@w<K}
8US-=>g^8`M}K@j9v3~Yq+HrlS^5x_C{w#E^tdu=QRK#xV=SPfwsrVmExsLP0<FczMGL>{sUSQShx9k
7)y%<bsx4!*zvn^BJ}l|xvxjwG9Gl#jYye!@43^;3o1AkE59^G)4}Q1>c5zd&U1u~C-JzmA_@Vxmg)D
)|bLpVvLV$1_gegdA{=cUb)@<^f!?@@sM!7)`e83<8bYP4FBFl%yY$tyT?t2}vUD<))vt#Y!qoK<`a_
H*MQ!GB*uJn@2f<$*0q^pqqJrUaD1E$&4J2wjG=}lYV`vbdL7DMB`GbvL1qSW%&{uL<X~~nOID3<`<K
Nm`|rmGSN0N8vcdgTO>rx^Uq4@9L!XG)xpk@qS)E`zGu>p{aY7SAvK(L8|=q|0)(qEiyW3k0!34nTp$
7FIleZUmR{O>^xexp%*qeBaL9(EF@)ruaP-CqTT3%eush)5)ZkvXbkAwe=JrsNyMfl;AJiT49i_|!qQ
iuJZ~KfbA<iHf*_$Mf6x@2MG^0hQ$$x~6SpIEUAsAZ-7*p>;u)l-|69_M)=G#MNq8Jk8gjVDjAyP6Ie
f=cOUY~IM_G=dgo$*ro75z@siJ34)S7rRVfGj<s5&7}bHq_i-P)h>@6aWAK2mofX{8-J$z%{@C0015V
000aC003}la4&FqE_8WtWn?9eu};M>3`O^T#obt*`VR~YY;QnfHmzwbC3ciJh5S8E87&>(bBYv517Wk
ANp~bsMyYmG$}2ukNeuDHNG^#ptMd*~JcpmA56q`#0W5TpB>IYnZ>tlx>JJR-$h|q#9KFT3l$ThGovM
`Z`h1@k{0zqrjTIlGh#re*%w%#go%(3HWDhs}=jz2OtQ*5LjXNW#DIpx4DusYoy!{s5eCbN6)&t+Mou
mghxP_Ew!2Ru`@Lf_lF*R=M@&`~$0|XQR000O8X0rTPQz>BIHvs?u0RjL382|tPaA|NaUukZ1WpZv|Y
%gD5X>MtBUtcb8d38~-PQyS9-R~=`vb0jUEJ#2l7?~<q*s2O$6DP5BxjWeoRsJ3)r62}wxu>V6=jZ2^
^8h*(N*&NpGAry!bPI1qDW?#fYiCKJ;y)-UvT=S?igML|#N0V|1C&T-+?m&U1H&i^Cxkl0h>f8(GeSt
y!hmM@*7^>0ZxDICF`IKwbq{?g1(QI~>zLfakj-+)%@|R<n`imIL!EOCnl4aU2kvC|v&LcG>LAL;BRs
)tPPl>FXUnWR2liI0)q792lR#k<<WI|Ni6O@Z>YOA;1gV*d3TSV!hA@Fx4{=_Su|>vITZ+Yw)Vl?|m_
=wBx}<;xHCT095Jc!zi|neZBkjkNuk%oqsf5b9u1I7=sqXI{AN)1o^8a@Yk4bqd+1TI9oO!O1FHsnE<
n%)>1#R3HP)h>@6aWAK2mofX{8&GLd6$3;006Wo000^Q003}la4%nJZggdGZeeUMVs&Y3WM5@&b}n#v
)mmF~<F*xk*RMdh4<TEUxjc0=QQN&}6Hm9cXV;rHqtP%F39VUEBm<DL6_5XW&p7}{fTX-hr!UciC4vV
B=klEk0DGSIsw>Kzt*c`p>gvF&mUWWnY+nmj$hu71qOMrpiK6<%WM0UY?QjM>E<Dd$EQ&)@i<Xu3r%y
PhA8ToTHEDZW7CZAOi<bAlPd!!3AKH77HjBNe4=k(8l4rQGWSZbg<XrIlO_8;Vrad*he|sa+jPKIy?g
mEt_b9R<`009`y#8VR`X3jU--qm?<s#jcJY?@cqmW%SxL8_->;s3#o36ok$Sh<ZD|od~Oq-&KlOwP4T
ErO_ZLu%R3ir1l-;}BWp;EL=eB?r+Ej9g*>TzIfUL?uBD0z~wRN`<_))_g$;$2iAKZqM=Wf4ozvjS#j
e%<gY(Svhy48MNDC*CFvI2ybZs)tVS{y}E9{J`fJ9eA7OX`9-7a=uTyvQ7AaC&k7ZnB&#8MJZzqqTWR
7_ph!#tk2W;#<fKd{Fkl}{P~q+w`)Y5aoJlTOUp7DhR;uJ`JqYjLiEsr=Qprm*4E+_GJFkhle?nIC4|
S`#oltk;4{M<$oYfThyw)Rv0vg^jlQM9#RAO)FIOh$Vo>`XjrmDZr3U~{uvjd>7YrPdca5JenQTSKcJ
v*v=&uUa8$$X9#<m*u8=}L3trAu6wi6ZeQ<xnvP$y+ytk{n6QgR%{m9jDgLnhaP?~4aDjTQ&(iZ)4n$
;*96nP6D|vaYxy#Sc=%NB~;lm-|A33=O<_o5G^QD?%m=4>0vT57r?uR>&rB`Rs~{Jh#$wW0{GfX{AdA
&_^l>WZHb1x{nL<tb)ean!wjp6(*Jhoa>XGps!LBvgP-@1@mEev$h63!D#TEvg=cO3z>mG@T_Z9UV?G
p#oAlWvQ7v9b9su8JE9$tvmmB7w*??rs+_Ioq?AntD2FPUSF#0&<8&)RU~&c1a2ZPL#MFw_*oaQwvhG
#!/usr/bin/env python
#
# Hi There!
#
# You may be wondering what this giant blob of binary data here is, you might
# even be worried that we're up to something nefarious (good for you for being
# paranoid!). This is a base85 encoding of a zip file, this zip file contains
# an entire copy of pip (version 24.2).
#
# Pip is a thing that installs packages, pip itself is a package that someone
# might want to install, especially if they're looking to run this get-pip.py
# script. Pip has a lot of code to deal with the security of installing
# packages, various edge cases on various platforms, and other such sort of
# "tribal knowledge" that has been encoded in its code base. Because of this
# we basically include an entire copy of pip inside this blob. We do this
# because the alternatives are attempt to implement a "minipip" that probably
# doesn't do things correctly and has weird edge cases, or compress pip itself
# down into a single file.
#
# If you're wondering how this is created, it is generated using
# `scripts/generate.py` in https://github.com/pypa/get-pip.

import sys

this_python = sys.version_info[:2]
min_version = (3, 8)
if this_python < min_version:
    message_parts = [
        "This script does not work on Python {}.{}.".format(*this_python),
        "The minimum supported Python version is {}.{}.".format(*min_version),
        "Please use https://bootstrap.pypa.io/pip/{}.{}/get-pip.py instead.".format(*this_python),
    ]
    print("ERROR: " + " ".join(message_parts))
    sys.exit(1)


import os.path
import pkgutil
import shutil
import tempfile
import argparse
import importlib
from base64 import b85decode


def include_setuptools(args):
    """
    Install setuptools only if absent, not excluded and when using Python <3.12.
    """
    cli = not args.no_setuptools
    env = not os.environ.get("PIP_NO_SETUPTOOLS")
    absent = not importlib.util.find_spec("setuptools")
    python_lt_3_12 = this_python < (3, 12)
    return cli and env and absent and python_lt_3_12


def include_wheel(args):
    """
    Install wheel only if absent, not excluded and when using Python <3.12.
    """
    cli = not args.no_wheel
    env = not os.environ.get("PIP_NO_WHEEL")
    absent = not importlib.util.find_spec("wheel")
    python_lt_3_12 = this_python < (3, 12)
    return cli and env and absent and python_lt_3_12


def determine_pip_install_arguments():
    pre_parser = argparse.ArgumentParser()
    pre_parser.add_argument("--no-setuptools", action="store_true")
    pre_parser.add_argument("--no-wheel", action="store_true")
    pre, args = pre_parser.parse_known_args()

    args.append("pip")

    if include_setuptools(pre):
        args.append("setuptools")

    if include_wheel(pre):
        args.append("wheel")

    return ["install", "--upgrade", "--force-reinstall"] + args


def monkeypatch_for_cert(tmpdir):
    """Patches `pip install` to provide default certificate with the lowest priority.

    This ensures that the bundled certificates are used unless the user specifies a
    custom cert via any of pip's option passing mechanisms (config, env-var, CLI).

    A monkeypatch is the easiest way to achieve this, without messing too much with
    the rest of pip's internals.
    """
    from pip._internal.commands.install import InstallCommand

    # We want to be using the internal certificates.
    cert_path = os.path.join(tmpdir, "cacert.pem")
    with open(cert_path, "wb") as cert:
        cert.write(pkgutil.get_data("pip._vendor.certifi", "cacert.pem"))

    install_parse_args = InstallCommand.parse_args

    def cert_parse_args(self, args):
        if not self.parser.get_default_values().cert:
            # There are no user provided cert -- force use of bundled cert
            self.parser.defaults["cert"] = cert_path  # calculated above
        return install_parse_args(self, args)

    InstallCommand.parse_args = cert_parse_args


def bootstrap(tmpdir):
    monkeypatch_for_cert(tmpdir)

    # Execute the included pip and use it to install the latest pip and
    # any user-requested packages from PyPI.
    from pip._internal.cli.main import main as pip_entry_point
    args = determine_pip_install_arguments()
    sys.exit(pip_entry_point(args))


def main():
    tmpdir = None
    try:
        # Create a temporary working directory
        tmpdir = tempfile.mkdtemp()

        # Unpack the zipfile into the temporary directory
        pip_zip = os.path.join(tmpdir, "pip.zip")
        with open(pip_zip, "wb") as fp:
            fp.write(b85decode(DATA.replace(b"\n", b"")))

        # Add the zipfile to sys.path so that we can import it
        sys.path.insert(0, pip_zip)

        # Run the bootstrap
        bootstrap(tmpdir=tmpdir)
    finally:
        # Clean up our temporary working directory
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)


DATA = b"""
P)h>@6aWAK2mofX{8+Vkj=%N*003hF000jF003}la4%n9X>MtBUtcb8c|B0UYQr!Lz56RfE?c3qp%k_
SHrQn_7~2lJl@i=UNd$>)BxNOkKc^)X0-?v#)8n-qN6<M@=zzu)S>cmJxA2{mV(^18RrQA~d8sORfnv
9}yTTaLU<;$CaPPU3^2R?b=Lb<f9y9wZ2He2ID^SqVK(3-FetQzg?ZW~i=PP*o`G6RP8AkL$p^XfaAe
?4Ml<oxLIY1qQ!~sESrlexcMesdSebdnOJv6AE2HAojLa&;nbgm=qr<1MY=+d0L%bJcvCKUI$e}1y7v

