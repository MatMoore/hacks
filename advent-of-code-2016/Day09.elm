module Day09 exposing (..)

import Html exposing (..)
import Time exposing (every, second, millisecond)
import Regex exposing (..)
import String exposing (lines, fromChar, toInt)
import Result exposing (withDefault)
import Debug exposing (log)


type Mode
    = SkipUntilMarker
    | RepeatNext Int Int
    | Done
    | FuckingBroken


type alias Model =
    { compressed : String, uncompressed : String, mode : Mode }


type Message
    = Step


input =
    """(190x9)(44x13)ZAVXETEBULPKEEYPUUMBWUPDHPXFDPIEWHXPNVMSKMMN(55x14)(6x12)VZQPAA(18x4)ITWIARZWEBBNFBLOGV(13x7)QYTKGAIZHUZAX(4x10)ITDZ(61x3)(1x7)Y(6x2)ZPMQZV(8x15)OIHTQPNI(23x12)CAXCRVLMLAKHPBUUODXQQNT(3x9)WJP(5x12)PJAMH(43x13)(30x13)RWAWRZCDEMSPYFDZVVUKZUWSEVFJWH(1x9)N(17x13)(11x4)YHEKAEQQQFW(3x13)SQF(195x4)(56x5)(4x8)PBWL(6x8)HWRMIA(2x5)QQ(8x9)JOISJLQL(10x3)JBKQBBPQGK(125x11)(24x13)ELKCLOFLJRFIJCIIRMCOZEPC(7x6)LWRTOXG(14x3)WPNDOOJCSZHKJA(23x10)VUBKGHFYHCEKZMNKIDYWIDY(25x15)FOFQQVCWHFRSRVRSYMYRCZRIF(141x14)(45x2)(12x1)UWTFPNJDKWSG(10x11)DHIUEFRJAQ(4x10)WSOX(53x15)(15x3)UHDWGLSDIHUYSMD(6x10)GALIPI(13x13)UBIUGFWYWMHCR(24x1)(18x3)SAGTVYELUTWSXQVWNI(10x7)GENZOXBYOG(4x2)RMGS(4177x12)(1752x3)(1513x4)(297x4)(10x5)(4x15)PBBT(160x14)(11x6)JCKLDJGYMGO(60x1)(5x4)SOMMG(5x1)MJENB(3x11)IIR(24x12)FQAMKJSXTZCAVAEDEQFQMWIR(70x12)(25x2)FWNHIGOHOUYCQSCUKSSCZXRJI(2x11)XF(17x3)VGTLRDJNDBERXWRAY(3x8)AJT(94x8)(68x10)(21x14)DUGIEEMZURLSHXEPSDMDH(5x11)LISKT(13x14)UMVAIVVRDTOSG(4x9)PGOV(13x4)(8x9)KWQGNJIV(8x2)RLEKKJWG(383x11)(75x1)(21x3)SBABSNIPBMLCXQECMVDGB(42x2)(11x2)ESWFOYEVFIJ(2x7)EL(5x13)OCVGF(1x14)J(189x1)(25x2)(8x13)SUFVDTKX(6x1)EOKRWU(28x4)(6x3)SRAGHT(1x15)H(5x8)VNPVG(24x6)(6x4)LOUBGC(8x9)EFISAKFG(9x13)XXKXSZNFD(73x1)(16x12)HOCOHBXNQRXTLLTJ(13x2)LGGHDLJZCIJOG(24x11)PHJDXXBUJTPSKMLGCALDLLGU(2x15)YU(91x11)(3x4)LMM(16x8)DYOHACMPKIHRDUVJ(44x9)(3x2)MDC(5x10)FNPGJ(11x1)OHPDVNRKRSI(2x10)YS(5x13)RURCD(134x15)(121x7)(7x13)XTFRZSM(70x9)(8x15)SNLOWPVP(12x9)MYKDYCTXIAZA(13x9)XMZEHDZTPTAES(13x9)TQLYGXTECVDBG(5x10)EXPSZ(15x7)GVFTLYYYBLGGUJO(1x7)N(14x15)WNZDWNHWJQOQNH(648x6)(83x14)(55x11)(2x13)RP(9x10)MJPOSAGCX(26x7)NXVQZQAQDWHABJFPRVMGSBACWU(14x15)ECVUEOUGLOEJUY(232x13)(30x6)(2x11)NZ(1x13)S(2x8)AR(3x9)DDI(45x3)(4x10)FFJD(7x7)ZRGGRXE(6x10)WJKSTC(5x13)NEQXI(85x9)(4x9)JCLI(14x4)HCVHVWLAFIUSIZ(4x1)BISN(26x2)HRPEKOHFGEJLJDGIWVLQOWJJKU(9x14)YXKJROSLO(17x12)(11x8)HFLFUQNVNMK(23x11)(1x1)N(10x13)TMNKWOOVPB(192x11)(26x1)(4x10)TCAP(3x5)LHN(2x15)DK(36x8)(13x13)UIDKJYPXBFPFO(10x8)BGWMNGEBRF(18x7)SIXYKHPJJONMMHQCRB(5x15)JGIRA(77x3)(5x4)MHAXO(3x8)WSI(15x14)AVHDFYABFZSAOJP(30x15)XNZULOJGEPQDRSHDYHHTBLEMRMPYSB(111x9)(75x13)(10x4)EBCINBYRMS(10x6)XNEZNHZJCE(7x13)HQOEZCA(14x4)OAIKFNURYAWDQK(5x5)VCRLS(22x14)ZROMOTQACGRYTSVCXIEEBP(16x13)(10x5)RKGNREWXGD(200x10)(77x1)(70x15)(25x5)(11x5)OEDHHSUIKNC(3x5)XKD(15x6)EIDHHIZMJRRAGSP(12x9)QNZKKKFEGAMM(110x1)(103x1)(74x12)(32x9)XABWGIVXFJVAMTILWOQXFNMJZSMAVHFY(30x8)TPBSRMCDOQNNAVZQPPZADGDWQAYWCV(16x2)WSDGMBKDJSOACIFW(2x9)XS(2401x11)(808x3)(1x5)F(99x6)(11x15)(5x12)BNHZF(75x9)(68x14)(12x13)UBFYCZHLDIRJ(2x2)EM(18x13)KNOLWZIARZVDYPKPPL(1x11)D(4x10)QFDT(136x10)(47x3)(28x12)(2x10)SO(8x8)TUBVOBJB(1x12)V(7x4)(1x12)R(2x3)TW(47x15)(40x10)(9x3)IPNMPMMCD(1x1)O(3x6)BKR(6x15)DOOFGK(5x15)KNCGF(6x3)(1x3)E(148x4)(9x13)(3x12)UZC(4x12)VKWP(38x8)(12x9)(7x8)IKLDJWW(1x8)I(9x5)FIBXVUYFN(72x13)(32x11)(19x7)SLSTSSNZPVSNIBPYQRS(2x8)UA(6x11)KXTTMX(4x10)MJMA(5x15)EKHFC(391x7)(3x1)DMD(64x4)(50x4)(8x9)IRDFCBWT(8x13)TKRVFJUL(5x4)DRSZI(8x5)YFTAAAZW(3x3)SYD(165x15)(72x7)(13x8)YXWPIFDIWTEBO(14x5)URQPORMHJUTGAY(3x9)HJB(18x14)VMTFPEBGKWWRLBODQH(81x4)(36x1)VPRXKSMKMDBXIPXGJMAGSEHEQLWAWRQWRIQT(7x13)RCFJLYM(13x7)FLKGGTMPZLEMG(2x3)JU(133x9)(15x1)YQJSGFRQQOLXAPM(15x2)NZUELUVNJDEECSB(56x9)(18x8)NMABOFTJAYZTEMSNTB(2x3)CO(6x1)ARWFWX(9x7)AWQFAIJNL(23x1)(1x7)U(11x2)HETPXKPHZAF(462x1)(171x9)(135x10)(74x14)(16x14)XNDDMDFQCZDHJZZZ(7x11)QBQIIIW(10x5)QNBFCGEEGG(16x3)QNDBYXJONNPSPHUE(25x8)(1x3)T(13x9)OJKYMWIWLTOKH(17x4)(11x3)FHYJYDFLLIP(22x1)(4x1)CLZN(7x10)RJFTIIO(2x12)MC(233x3)(3x7)AIT(40x5)(10x9)(5x1)LLWPV(17x11)WJGWFPRRSEIQAJYMM(36x2)(21x9)(15x2)OCWZSWWKTBYNHHS(3x14)KPF(105x3)(6x11)UCHAIT(25x8)(18x15)PAEPDOQFZFCOWXNKPM(43x1)(11x12)JFQAUNYHERQ(9x11)DRQITRCYP(5x3)WTJHQ(8x8)OHJBAFIB(19x2)DAFUAZEEDQNGIZRECDJ(1x1)P(24x8)MZPCRRIKUHWFOHDVOMNLOBMO(217x9)(209x10)(25x14)ZTSIKFJVMLJUQETBKJPPRTQTS(6x2)VAFWIN(89x5)(6x5)(1x7)X(71x14)(2x5)OS(16x1)VIBKGDVQXIBHAKNI(3x5)ZGR(19x14)MLKEFZKKQSYHAELTBGB(2x10)CD(65x4)(58x12)(3x1)ZIU(3x12)SZC(10x2)OQPHJZCGVW(9x2)BDWHFXWZX(6x2)PTHTDS(885x10)(613x1)(38x15)(11x10)DUOYNEGCCAP(14x6)(2x11)ZT(1x5)R(232x7)(25x2)(18x14)QVUIOCQAEZLOTZVXIX(77x7)(22x15)HVHLSATCKEFKLWYRPJXKSI(3x2)PNW(33x12)UTZCGONSVMLAPWTAZILLBRNDOABBZBLRQ(11x6)VCKFJVKSNFC(3x5)COU(86x11)(8x12)YLWMFUKC(16x12)HKQZWQXAQEZELTKJ(6x4)DKEVJB(16x14)WKKMITBLHTJDDIBV(9x11)XPSECVOAO(165x4)(62x1)(11x3)LBEETPNBLEO(5x14)RYYQP(5x5)UHLVY(18x2)OONYEICVPEDLQHIUSJ(36x4)(30x4)KQGSBKSAIDHYDRXEBMNLIHLYXVPEZH(8x13)SYVNWDUT(34x12)XLWWYVKPHEMTJBEQYGKHOQDSHVAGNVMFJK(139x13)(27x7)(1x5)C(4x15)JBBW(5x13)AJJKR(56x11)(18x7)MIPUIIWUHSWCQMEGYN(6x1)MEHVUR(14x11)LOIATKARYOHUJU(37x6)UVKYKHPRZUJFSTUUKFTQIIKKNZOLCQLLBJXVV(5x7)NTEYE(258x7)(33x2)(4x12)EAPG(5x6)SFYVB(8x8)BPGFSFVY(57x7)(1x9)S(44x11)(2x1)RO(1x11)S(24x1)GDRUIEUMOHITSMXDIDGJARJQ(15x6)(9x13)VJZKHBRCR(127x10)(23x12)(1x9)V(3x4)HEI(4x9)OFWY(10x2)BBSZRMWOHR(7x15)(1x15)M(31x5)CKEZCRPSEGEZDYRPWQUKNPMCBTNSPAI(25x5)(1x9)J(12x15)BSSMRDPRNPDY(3785x8)(8x3)GHOEWPFD(1806x14)(124x10)(105x8)(10x9)CDDMAEIXOO(37x3)(10x4)(5x5)VPMMI(3x5)GBP(7x14)VJHBABZ(18x14)XNTKDFTRBCZEACZALZ(14x12)TYBGBOIYRCVRZU(7x2)IORHKKB(590x10)(54x8)(17x6)UTOVYCYKDKKEIUCAI(25x9)(19x6)HIWIXDNGZZJGIACNPPQ(523x7)(41x4)(1x1)I(7x4)(2x6)GU(17x1)DZVZPWJUHXFIHHPFP(196x13)(5x7)OSDSW(15x3)SRTTJWWSYUJGBFF(27x2)(4x13)MSYH(4x1)SXNR(3x2)DPR(70x2)(16x13)QCNXMJXCKTMHZPBM(2x10)FO(25x6)AEVXNJGKTBCPMCUASWXOWHAQS(3x8)GOG(50x2)(14x9)AAGJSTOOBANCTR(14x5)MDCWUWOSELBMGX(4x10)YYLT(10x15)SQZZGFJLDT(133x13)(57x11)(7x11)DDNXMAC(2x12)DV(5x11)UBANO(19x6)NLORMPBFFBOYBQIBZWV(6x8)ASEPWF(21x12)(14x12)FHGWBAXHALMVQI(17x7)(10x13)CCDGPEISBV(2x2)OX(107x3)(7x1)QNMWYFE(18x3)LMFXMYUQKABGXVOUVV(7x9)(2x1)BF(37x15)(12x8)KTBAPXKZLKWT(1x9)W(8x1)GSDNJDSU(9x15)KYVQMDMQW(593x4)(255x7)(146x11)(40x9)(33x12)YLECKKJDQVAMUFFXPWGHUSOECCHZXBLWM(93x10)(3x10)BXC(1x9)U(2x10)BF(18x10)SGORQZUALUTFAVYLPW(39x9)WQGBTEVNTRHTIWQAWVJKIXJVCVMKRGQMPPMIFSF(94x13)(88x1)(5x11)EEUOH(31x13)FSLFXZCUXOXHREPXRPFAWSEABNPADCE(5x7)KEMTG(4x13)GDAZ(13x1)JCRZXVSFBDJZK(4x12)SITF(269x14)(24x3)(7x13)YXQHGKY(5x14)ROOVW(205x14)(10x12)ZZBVWTQWEV(56x11)(1x6)R(10x6)NFOTUTICTJ(8x12)JZWVIHBE(13x13)UBIZNBBEZOIID(28x2)(14x14)HLADLLCONGEPXC(2x2)NH(9x14)(3x15)YCB(69x11)(14x13)QXFXOJBHONIVVJ(5x15)YJMER(6x12)ITSZWH(18x12)IGLEYGQAABOWKMXFGE(20x3)(14x5)(9x7)MSOAXHAID(38x3)IZFZRYYEJVCORBDLTYOHLZHKVDKQVADYQISGTW(469x1)(18x3)TWUUVIXHGSCVVDOFDJ(437x12)(86x8)(40x6)(19x9)OSYGQMGNNLPBKXEPHQG(1x12)M(3x2)PQT(17x15)TQQBGULRUKIXBPYZW(10x7)(5x9)TZMKP(75x3)(68x14)(13x7)QTDRLDGGUIORW(9x10)JTAZPINDH(17x12)KEVECGSLNRMIRBAZO(5x5)DVTUL(199x6)(60x4)(13x11)NWEDTFZTDQWFY(3x3)JBP(4x4)PYBQ(16x11)XZRNQJPUOMZZMYYR(77x2)(2x15)ZK(1x11)V(3x5)BRV(30x13)NLHYJDBXRMCZOQRFXABZUZILEHZMZX(11x9)QONGFLBHCQU(26x3)(5x4)WWVVY(2x15)ZH(3x7)MDR(6x3)PCMRSD(2x1)AA(2x14)PG(44x3)(6x1)CVWMIH(7x13)HSQHXKD(13x14)(7x11)WGEPOEK(1507x5)(39x1)OMGCAFYYXDFVRVNEYPBATJCKBHTRSMGIWTDNIFP(21x9)BDIJRNXYMIRXXILMGIFQK(404x11)(23x15)(9x3)MWBTTYJCT(4x4)UEQO(15x10)GUYNAWLCLNHJPXD(5x5)CECRY(334x14)(67x10)(60x14)(4x13)ZBQU(3x7)SJI(3x14)GKR(2x2)YJ(20x5)DJQTDUIFRGDDOOAMZSFM(99x13)(47x10)(14x2)THIPTHUFVLLGXK(11x15)SQGQIYAKKOC(4x4)TNIC(38x10)(6x6)KCQRSL(3x8)JZT(1x11)B(7x1)XFDBCCU(147x3)(8x13)SWNXWSCS(18x5)VDRJWFBVUTWDFZDCLM(62x3)(19x13)NFZAMEONWPPNGFFODDP(14x13)XTOZXOYZJQBPQC(9x12)AOSMZPGZV(8x13)UZOKBJJQ(21x9)(3x11)PFH(7x4)JDSYTAF(1014x11)(386x14)(119x5)(31x6)ORPIVAGZSMEQRAAOQRSMOAFFWVVFBDT(53x1)(5x8)PRHTO(7x15)HXUNQUA(15x5)AJAJOJCLVYZBICO(4x4)DHZH(3x15)BWJ(9x6)TCXBOMXXL(190x13)(54x15)(3x7)OKI(8x11)TPHKZGWA(6x15)RMAXEB(2x11)QZ(7x7)BXCDHWF(14x11)KYUHEMBXSEADVP(49x4)NLMONTYNOIDPEALJJBKPLWHCKBVVBHHUZNGUSULFWUAEBQQCQ(47x8)(2x11)WJ(8x11)ZYDVAWLX(1x6)W(6x5)CJIWBA(2x15)LS(12x7)PEYJTBKWCUPT(38x2)(31x14)(2x2)CL(17x12)ABAKPQWMMGJTORRBB(4x12)GHGK(496x13)(231x7)(60x2)(11x10)PHJQCJOXFHA(6x7)BKEVJY(25x5)MIZCFGZJRGZDMKHUEGZMACELH(27x12)(3x9)SMI(12x15)CCJWNFNOUQGC(101x8)(27x15)PPDYHKWCWZYEEJJPUFXRRYIASUT(17x10)GGFQFHRYKJMXKBBAR(8x3)FTPTBVXE(23x10)CLAVUXEHWTEYZQNRYOGIQME(16x15)(10x8)LAZDAYDVLM(193x3)(9x15)OHPJACNZL(40x14)(1x9)O(17x7)UOFNZKLKAAMBPOHNS(6x6)SZIJWV(54x5)(2x7)FV(7x9)GEWYULA(1x13)U(22x2)ZVSVOAJXMDEMUPOQLTINZF(24x15)TWQIDBTWEPQBMHYKPLYZSVZI(33x15)(20x1)LZUNQTUVMDOOXEDUZFAR(1x13)K(52x3)(46x9)(7x8)WQWZCBB(27x14)HAZIUDWNIFUKQCAWYFJIGEWSLJO(85x12)(55x7)(48x14)(3x4)TBU(22x6)YFSPWGIYYVLXKMNBKZRFMH(7x1)LGZSHDG(2x10)HY(10x2)SLXHMEWSGF(9x8)(4x2)RWUE(434x11)(426x14)(52x8)(21x14)BCBITAXHZMXHHYRZDNOJA(18x1)FKEHYEEXRRMXDUPPLZ(361x9)(127x14)(29x4)(1x11)G(3x5)TXQ(9x2)KKWGNXDII(11x11)RVLXVHDTCUP(68x9)(11x8)YQKPSJFRDFP(16x10)UUEHIVBUTUFRUVDE(2x14)RX(14x8)GVHHPSBTEJUNKN(219x7)(105x11)(21x10)EFKAZUOPPUTTNFYUNJSZO(71x8)HDPQUFFZUXYPEKOWXNNZVQJFIZEYEODJSNYUOAZOIRQETXCRZBGJWWMMPPIIHJEGFYREGNR(38x11)NKGEVBBLDDLGOYUHLBWXSEAQHFNGABJENZQMVU(3x14)TTC(34x1)(6x10)NXQLWI(15x10)EQVLORVBUBZDUMB(7x8)(2x7)VA(5917x1)(2328x4)(814x14)(37x14)(1x10)J(24x6)(17x10)TRMNJJCWQUYENUBXU(445x15)(177x1)(37x14)PUCBAZGPSDOVSUSSZSCCWDCWYILTSEMJVIVZX(17x7)IMEOLAHQLTARXBTDR(65x8)(2x5)YN(14x12)QXEQUHYTHIHLPM(5x5)MTCMS(9x6)FGQLYLJNL(8x8)KHHJLUDZ(32x10)FXSLPGRBINYRWGIWKRRYSEWARGDQDPSW(10x10)WLADYFJIUQ(2x4)XX(209x8)(94x11)(36x15)UKGUJGLESXQIOASTZHMRHEWIEMXOYYIJUKAG(6x6)NCIDZV(7x10)JHACUVQ(21x1)KAGYAGPGGDOGOBXMSNJEQ(91x2)(30x15)UUMCWGDYGHNOBMJTPPZVSZEHNKZCAA(27x9)VXBDEFDWMTIRGHCQSYDYWCSBJPY(8x7)GKMVKFZJ(2x15)NS(5x14)BPRCM(15x3)OPXQHISSCCOQIEA(287x9)(280x8)(21x3)PKYXLJXGOKXSXBZTGDEGK(59x1)(12x13)VGTKVMCQIXTS(2x11)BF(1x14)W(18x14)JDKAOKYPNNXQMDKKGX(7x2)IHUZYBL(73x4)(9x5)FOVTPBVAV(13x9)EARZLZXSPEGWQ(3x3)QAR(11x12)TWJVZZSODUV(9x5)CGFVAEEEH(90x15)(11x9)YWKHVDSVGUO(12x10)GENMNJXISQVW(12x10)KBTDARSOPYAQ(14x3)NHGNNHWJAAESBB(9x10)CJIVXCNIZ(17x5)(2x10)VL(4x1)SSQH(430x7)(202x4)(1x10)O(187x11)(4x3)LYVC(94x5)(2x11)YL(37x5)PKLWZVRFRDJNMQUYXZZOGBUCFEGKARHPZRWLH(12x4)GJTFJWUZZGDJ(11x12)PQYMGSOEGFN(1x11)E(13x6)SMCPDDOIVMUJG(43x7)(19x1)ARSZUFFVAWVUVVAJYZG(11x10)DBEQVCPRXFZ(4x13)CILW(19x14)SOMYRGMAZBGXXSSVQQT(188x1)(2x7)OJ(19x1)(4x14)NIUS(4x5)MZXK(149x5)(5x15)XJJFF(9x3)WTNULIFAC(3x4)IEG(6x14)BUUOSC(97x15)(3x7)JDE(21x14)DRSIEZJSCSARMYNLHBXMA(6x6)KLXKVG(23x10)GWFKMOJCXJAZQRPYSIOJJMX(14x8)UVPDUFZQCLWMRY(1041x14)(487x4)(147x5)(18x5)(3x3)IEG(5x3)ORYNF(39x10)(2x9)ST(7x3)CNEFQLW(5x1)DWNFO(4x10)MENC(71x7)(10x4)WPXANNVOAW(9x14)HMVITPUDJ(2x12)ED(19x12)QFRXEDUDYNRCRGIQACU(1x4)G(153x2)(2x6)YX(35x7)(3x14)UFH(6x6)JKPPKO(2x14)NJ(2x7)UD(80x15)(1x12)W(5x13)TLUOY(12x13)OGETDQFVRFHB(30x10)VXWLNWQFZIBHSHJFUVXGMWQKRTPUNW(1x5)B(2x10)XJ(5x2)FLSQR(86x15)(64x9)(12x13)FWBFVBRJLSFO(9x10)ZPRGOCGIY(1x4)B(17x10)GLFZZASOWKMWKPDTX(10x8)CAFLEOCKCZ(54x2)(10x8)GGUJBSQXKH(1x13)K(11x2)XMEFKFUWGKB(9x4)AUZEFUEAN(13x14)VXYFVIJSRAVZZ(223x1)(104x2)(81x14)(29x6)IKMHIQWEIAZRBLNRYIQEOGFYMUCEE(3x12)NEU(20x15)RSUTWKPGWJJVIUDYXASE(5x1)YWRMT(10x3)VQUXAKOZAF(105x4)(2x3)AW(7x13)DJVQXBD(20x13)(9x4)DXROACCWK(1x4)O(26x13)(1x5)H(13x14)SBMKWBSXIQTUZ(19x5)GSHERQSGPSGZSAAODTO(309x10)(15x14)DNIEMCZLWCGEGSR(109x4)(1x14)G(45x5)(7x5)JTGEPNX(7x13)CNJHWWK(13x12)KJWMEKGRJRMQY(44x11)(9x15)OGVNXLNGE(16x11)NHPXBCXLHBHZSAQB(1x4)L(93x4)(7x12)(2x3)OB(7x4)SZLFMBQ(62x2)(2x4)OG(1x14)U(5x4)ZNTON(32x3)OEIHONIOMNLTJSVTNHGCSLRJXXPQURCA(66x1)(54x5)(15x9)LYQASFYTPBJCCTQ(5x13)GXJHJ(9x2)GPSBRVISD(2x14)RH(1x7)K(12x12)(6x13)(1x5)J(864x10)(216x7)(178x10)(1x11)G(154x11)(90x13)(12x12)UFQPSXIWWDUQ(13x6)FYWZJVJNQSKEQ(15x12)GSSWXSFQVZTXGOG(4x15)MOQA(14x3)YHCUXXWSJYCNQI(50x13)(16x7)UPECXWSSIGLSAZOP(2x12)RI(6x15)WWABBQ(3x8)BPI(3x11)NFV(12x9)ZYSZENNMCSPP(6x12)(1x1)P(315x3)(62x11)(55x13)SCWUEOTJUJEMXZCCKXLCTEJVIRXGIUJYKUXGWLAOPECYNRGQPDCOSQV(210x2)(7x15)(2x9)XX(153x6)(47x2)(4x2)UBGL(1x4)L(2x12)DX(6x14)MXHGZC(7x9)LWFVNCK(70x5)(7x5)UFXBNXP(7x5)PKQATYS(11x8)LHGQTJWLAZJ(13x14)OFBRVKMVTVBZZ(4x6)XWEG(9x7)GSTAYQFTU(5x6)TDRMT(5x3)HJYCR(12x5)IWDWYJNQWREP(4x9)YUJV(11x6)KMYUKTMGGXM(7x3)SURQLZX(311x14)(74x3)(8x15)WQZPCBEW(33x12)(27x3)(11x3)YUVMRYKBTVB(5x6)NGWOQ(13x10)(8x5)SBGOAMLC(223x14)(216x8)(132x3)(21x2)PDWWLLVUIJDBVMBAPPJZM(3x13)IYX(8x2)GIANHKIZ(69x11)BAKSUXGMPAGTWYBQTTGVDJUIRLJAFSLFOKSDYHKRDXLZUYFAYSRWLVQQVEZXXWLOVXQUM(1x11)X(6x2)ABRRNH(15x9)GMKKGQJJGUTMWNC(6x15)(1x4)I(27x3)(21x3)OOAVOEXIZFFOLRTUKQNPH(19x3)(13x1)YLFXGZKVYIPCZ(2656x13)(857x8)(30x10)(6x3)VEIEFD(13x7)(8x2)OFNGTNFE(214x14)(5x6)ICUDF(48x12)(31x7)(2x10)TP(7x10)WZVHLAL(5x7)KSICH(5x15)FVQMZ(7x6)AXHHPXQ(130x8)(11x14)PVOXSOISUKL(62x11)(10x14)HGAHGPYOTZ(9x14)XATSJXSGN(3x13)UHW(7x5)BDFILVO(3x15)GMG(37x8)(3x12)AMM(6x6)LOPLLX(10x10)YFQHLBVIMU(228x4)(196x6)(72x8)(2x8)UY(12x5)SBLKPHOBOVFN(11x15)WLTYGTOAQWA(11x15)RMCCQHSJLXA(6x9)YMIKNU(50x5)(3x1)UTD(15x1)ZQIGJQRVLIHWAXA(9x2)DEJZUYIAL(1x10)N(55x13)(2x5)JX(9x11)HIBOQBDTQ(3x15)DZW(18x4)EWTFFMXDRUKNAPRHRA(8x1)YWZNRIBZ(6x14)IYSFIN(355x14)(194x12)(69x8)(3x3)JWI(11x1)MWECPWERVLX(25x15)YETRDSRTQWJVQLUJMBAPEDYJS(7x3)ITRTVHQ(10x10)LCXBZSSHTD(2x15)YF(53x1)(7x5)NOKQXWK(9x14)KZWHIQACE(5x1)YYBBF(10x2)TIVHXKIADG(29x5)(2x11)WH(1x12)O(1x3)J(3x3)DMD(146x1)(103x14)(3x3)ERJ(38x9)GNCTOAYQMPVNQRIVMPVHFSSSGJJSSKSIDALFXX(4x1)NCQT(3x14)LET(26x14)TFTZFNESHNZTQJXXYBMSRWGAGO(28x15)(21x13)GRQXOPFOMEVVQLSLETKMP(868x8)(2x2)LQ(413x10)(16x4)BJDCAOAWPRKTUFRC(31x15)LHSNRKFAVXIRZAKFIYGXZPTCIRUNZHG(193x3)(121x4)(2x6)WL(18x5)MXOBIDOXCQZZZQZXYC(5x10)RNAJG(38x3)QVEWABIGEWSUMFJYHZQLBTEDHDFIYFVMXHCRRE(28x11)VQEPBWKREZPTIZFUUNGEMZMXHFZS(59x9)(4x12)NCCS(19x9)JYSMUMHFWZFPABRIEEA(9x8)UFKXIDPNI(5x6)SGDUG(146x4)(28x5)GQKNGDPHQEJTRWPEVQJYFFIQYYPF(28x4)(15x10)AWEFQWTZFCCLXKE(1x7)M(13x8)QBKRCQRRBJDAE(53x1)WANGCZVVKGDRBZQRAVCUZMMCGNJNSHNFXANYREMTHLBUQGGZHSHHA(17x13)(3x11)BXL(3x8)RNJ(359x12)(17x1)(10x14)VPPYMRFSRU(207x4)(90x2)(21x14)VUDTSKRNATYRMYKGYQYDL(36x9)LDLIDFVHNZNTJTSSEYXDGRVODTLKEEZNOLFF(1x7)X(9x4)MGCIKCCSN(10x6)FPZMNVWKXH(24x13)OUBLSXEEYBRLOLVGZDQWDLRS(58x1)(23x13)WINJZLMDVRARNTFALJISNQK(4x4)QSQK(12x10)UPGRXOKUXTDM(115x9)(2x2)HO(21x1)(8x6)PCXYREJW(3x1)UWY(57x15)(6x4)QYSTVV(12x13)VRHZQVQAUZZX(2x10)DE(3x8)VGE(6x9)NXXMWM(10x15)MIENAJJIIE(43x8)YVIJLFYFOEQGUPNDWTRHDCLNVFGHIAPANTFZAMFGJQC(327x7)(3x11)ALX(311x1)(231x11)(25x11)RGXIXRXCNBRIFYSSQBKJXMASC(47x6)(8x12)OIQIUAOX(4x12)IILJ(17x7)NXBRGOKPSBULLIBXL(70x2)(11x9)GARFKGTCOJL(10x2)DXLRJCFRLN(17x12)FLZSXBDSLPOPDFFEM(7x12)PHEQJMO(5x3)JDOEM(54x4)(2x1)TD(3x4)YSO(2x14)YK(17x3)SSRTVCFNRLIKNOFRP(2x12)HB(24x1)(18x4)AZJCRZPJNIDEXSAGWI(1x15)Y(15x12)SPBYIMRXHEWUTGI(8x1)TGFEVRJD(126x12)(119x4)(6x4)AQOOFZ(101x7)(59x10)(22x12)SJEEKAXVKZYKJCXXAWWNEG(8x12)WGKCHMBP(2x10)KQ(3x6)MYL(2x6)VA(7x9)(1x11)K(2x3)RV(4x2)GIJL(441x15)(408x13)(289x8)(43x2)(6x9)BQAZCP(7x13)IZBNZQI(5x13)ZGMYF(3x4)GMZ(78x1)(15x12)DNXKBBTWSCRPEML(23x10)WAYXCNEKHTIISDIQEWGDCNF(4x10)XQRB(10x3)OISRGHWVVU(65x7)(8x15)KIFIOIVA(10x12)WKMUSFSYTC(1x12)U(8x11)JSNCQHWS(8x4)HYCCNHFC(10x8)(4x13)BQCN(63x2)(3x2)QGR(9x12)TOXGGUVRN(3x7)COD(25x14)CMLKONRWTLWLVWYUUEPWSBTEZ(72x8)(19x12)ARIOAFCAISJRQDMDHOF(24x7)HGLXAYCAYXGUWPYTOXGQZWLY(10x1)(5x6)PRJUZ(8x9)(2x12)BH(9x5)(3x11)MXX(2x1)XJ(19x8)HNLSLARKZVSCFTEXCSI(13x2)JVOICRNXKBEJW(2422x8)(10x15)JYSIQCFZOH(2369x9)(17x3)BWRHXTCEWMIOWCBLZ(1509x13)(570x6)(246x14)(60x11)(1x10)P(3x11)HKJ(8x15)IWETKXOI(5x8)NEADO(14x1)IEAVMTLUXBXBDE(8x15)QBBQUNOR(51x4)(45x4)YCCREIRLYPDFFQVRVJLOXIKRTRMDMBKIRVKHITINOULDG(15x4)WIDWCKTMYZPSREB(80x10)(7x15)ZVNHHAM(3x7)BHZ(25x1)PFVLKTHEUATHNNGXYDZGIJIBK(16x3)LUTCOWZBFVHJTUBK(1x9)K(190x15)(14x4)YXOTSDWQOJIVDW(53x11)(3x13)CSD(5x12)SDBDT(27x7)YDOBGKBLGCECQIVSRGFGIIJBWGA(30x7)(3x2)JDT(16x9)SFFCTBDYOVMUKMPL(51x5)(1x8)E(4x3)BITK(15x7)FLWVPMCSZRMVWYV(9x15)EIJVRIWJA(11x8)CSGGGGATSAO(83x15)(68x11)(14x2)LLJVOPOHENDLAQ(3x7)DVN(2x3)YS(11x3)XSBUFRQPHOY(10x9)WVHAUYCVEB(2x13)OR(6x10)OSFCFB(10x6)OBBFPHGWAQ(30x4)EXARKTZXSTLIHCZZRQACWOPVJKZGSK(394x5)(86x10)(9x10)(4x4)YPKF(16x12)(10x5)AVCMULTYPH(28x5)(8x9)WRCBEQLZ(9x10)FDNRGFFOE(8x14)LANMMNWZ(47x10)(31x10)(1x6)V(2x3)RV(6x9)YUCWZK(1x11)B(4x6)EVKQ(30x6)(17x6)(6x5)QKMAXX(1x1)R(2x8)LC(204x2)(13x13)(7x11)BANBCOT(81x7)(2x10)BK(56x7)WBGFHSLVALLDLXHGVCQOAHKOFKAEVQOKSVRBIGNGGIYDVXVWOQUTUEMM(5x10)XGTUJ(58x13)(5x3)ZQYHT(14x4)ZZGNGNSJKPSGRQ(3x8)AKN(4x6)RXLZ(6x2)WEEFXH(25x11)TJFFJBAAGGOBSAZQMQUICAHYI(236x9)(194x15)(3x14)JVA(35x11)(11x2)GQGINADTCQS(11x12)RTIRLMBRRJH(61x10)(7x13)CBWDCZV(7x10)JVCBFYH(1x12)H(13x3)UGATYZUHDCEYZ(3x12)OVG(7x7)EIACOSC(56x12)(27x10)YNDHNMITCLTBYSXPTQUTOUCQIXT(15x13)MUOBITUAHZJSRFK(27x10)(14x12)LXCRVIHJNXRIBA(1x6)K(244x13)(25x5)(6x11)(1x4)T(7x10)SRNQHTE(86x10)(14x9)VWOSJAUKGACGWY(22x12)IOCFRYWTITQHRWWRGQVYDN(14x4)PFETLTSAJBRKLD(10x10)OJCWMEHWKB(50x13)(44x9)(26x1)JXVEVGQUOGOOUTKSOEJYVUBIQB(6x14)ZLEVWS(57x8)(23x4)LYXFADIWRECSPOFSVZNGBHV(21x13)CKUEOYZWLZRXIMLRNIUXP(820x13)(261x1)(144x11)(1x5)E(64x1)(18x13)FCVQICIADHEWSQXHWE(26x5)XXKJGNVZWFOVTEYUREEFCHICDM(2x5)HK(15x11)(3x10)ORP(1x8)C(39x11)(4x13)SUFP(22x10)KYQUIAWLMRKSIOWRBRDWWZ(27x6)(21x6)(5x14)GPQTG(5x2)OPMFU(1x14)X(63x3)(57x4)(6x1)IQFWVT(23x14)AVBLZTVEXGPWRROBTUNYYNI(10x4)DTKMOIKVHV(297x13)(134x14)(2x11)HZ(46x4)(16x4)VZZRZCXCXQRURHKS(11x11)VUEMWTKDREM(1x9)U(35x3)(6x11)YNEWZL(16x12)QMHAUQCYJZCYLMND(13x1)VREYZNFSUNKMO(8x13)RLWWXNXA(13x13)EGENXEUKVVSUI(31x5)(3x2)PGY(3x15)RWD(8x15)YRNZQEBO(16x6)(10x9)(4x10)VLXQ(70x3)(6x8)TNVWPK(1x2)A(46x12)(7x9)HGHIFJD(3x9)JAK(19x11)CCNIXNDAIXLLURONAJM(4x6)GFMK(231x9)(187x6)(16x12)KLYAJFBPAXQIVSLJ(4x13)KHJZ(61x5)(23x1)WMHPHZFOQDFEBWBLYWHUVYD(17x13)AGOTHNZXFDKTSOWER(3x9)OEK(37x9)(6x2)ZWBDUY(2x3)DK(12x15)JDHDZQWPZOJU(38x1)(4x6)NGKF(1x15)I(16x5)VYLULCVBLWHGFXWU(6x5)DBKVCG(11x11)JZESDFRQABC(3x9)KDK(10x1)(4x13)AABI(7x5)KLEGJFL(10x5)(4x15)ZWUS(8x2)QFDRMQGB(13x6)(8x5)(3x8)CGU(20x3)SRQEHKTTHHVEZBPBXYLJ(3x12)BUI(27x2)(21x8)(7x12)IVFOQOK(3x5)HAG(45x15)PZDPOLVYNVIARZUFYFYFSCRUBGUYFOIPJFWRQBFNPTTTU(26x13)(3x6)AGP(3x11)ROD(3x13)HAW(63x6)(2x10)TO(29x12)VCQIALMPBPWQRPGGDTYLIDVQJBVND(13x9)(8x8)UUNJYCJW"""


testInput =
    """A(2x2)BCD(2x2)EFG
(6x1)(1x3)A
X(8x2)(3x3)ABCY
"""


init : ( Model, Cmd Message )
init =
    ( { compressed = input, uncompressed = "", mode = SkipUntilMarker }, Cmd.none )


fuckingParseTheInt string =
    toInt string |> withDefault 0


markerPattern =
    regex "\\((\\d+)x(\\d+)\\)"


countNonWhitespace string =
    String.words string |> String.join "" |> String.length


decompressStep : Model -> Model
decompressStep model =
    case model.mode of
        FuckingBroken ->
            { model | uncompressed = "This shouldn't happen LOL" }

        Done ->
            model

        SkipUntilMarker ->
            case find (AtMost 1) markerPattern model.compressed of
                [ match ] ->
                    let
                        beforeMarker =
                            String.left match.index model.compressed

                        afterMarker =
                            String.dropLeft (match.index + String.length match.match) model.compressed

                        newMode =
                            case match.submatches of
                                [ Just numberOfChars, Just numberOfTimes ] ->
                                    RepeatNext (fuckingParseTheInt numberOfChars) (fuckingParseTheInt numberOfTimes)

                                _ ->
                                    FuckingBroken
                    in
                        { model | compressed = afterMarker, uncompressed = model.uncompressed ++ beforeMarker, mode = newMode }

                _ ->
                    { model | compressed = "", uncompressed = model.uncompressed ++ model.compressed, mode = Done }

        RepeatNext numberOfChars numberOfTimes ->
            let
                skippedChars =
                    (String.left numberOfChars model.compressed)

                remaining =
                    (String.dropLeft numberOfChars model.compressed)
            in
                { model | compressed = remaining, uncompressed = model.uncompressed ++ (String.repeat numberOfTimes skippedChars), mode = SkipUntilMarker }


stepThrough : (Model -> Model) -> Message -> Model -> ( Model, Cmd Message )
stepThrough stepFunction Step model =
    ( stepFunction model, Cmd.none )


update : Message -> Model -> ( Model, Cmd Message )
update =
    stepThrough decompressStep


subscriptions model =
    if model.mode == Done then
        Sub.none
    else
        every (100 * millisecond) (\t -> Step)


view model =
    div []
        [ pre []
            [ (model.uncompressed ++ model.compressed) |> text ]
        , p []
            [ text ("Decompressed " ++ (countNonWhitespace model.uncompressed |> toString) ++ " chars") ]
        ]


main =
    program { init = init, view = view, update = update, subscriptions = subscriptions }
