import os, re, configparser, random
from mml2mfvi import mml_to_akao, get_variant_list
from insertmfvi import insertmfvi

JOHNNYDMAD_FREESPACE = ["53C5F-9FDFF", "310000-3FFFFF"]

used_sample_ids = set()
song_id_names = {}
song_name_ids = {}
    
windy_intro = False

class PlaylistEntry:
    def __init__(self, name):
        self.slotname = name
        self.file = None
        self.mml = None
        self.akao = None
        self.inst = None
        self.variant = None
        self.is_legacy = False
        self.is_fixed = True
        
class Playlist:
    def __init__(self):
        self.data = {}
        
    def __getitem__(self, key):
        return self.data[key]
        
    def __setitem__(self, key, value):
        self.data[key] = value
        
    def dupe_check(self, name, module="unknown"):
        if name in self.data:
            print(f"warning: in {module}: duplicate playlist data for {name}, overwriting entry with file {self[name].file}")
            return True
        return False
        
    def add_fixed(self, name):
        self.dupe_check(name, "add_fixed")
        self[name] = PlaylistEntry(name)
        self[name].file = os.path.join('data', 'music', name + '.mml')
        used_song_names.add(song_usage_id(name))
        
    def add_random(self, name, pool):
        self.dupe_check(name, "add_random")
        self[name] = PlaylistEntry(name)
        self[name].is_fixed = False
        pool = [p for p in pool if song_usage_id(p) not in used_song_names]
        if len(pool) < 1:
            print(f"info: pool for {name} is empty, rerolling playlist")
            return False
        song = random.choice(pool)
        
        # check various possible file locations over various possible variants
        vbase, vid = song_variant_id(song, song_name_ids[name])
        sfxmode = True if name in ["ruin", "zozo"] or (name == "assault" and windy_intro) else False
        for searchpath in [os.path.join('custom', 'music'), os.path.join('custom', 'music', 'legacy'), os.path.join('data', 'music')]:
            target = vbase
            potential_files = {}
            found = False
            while True:
                file_to_check = target + vid
                variant_to_check = ""
                while True:
                    mml, varlist = "", {}
                    if file_to_check in potential_files:
                        mml, varlist = potential_files[file_to_check]
                    else:
                        try:
                            with open(os.path.join(searchpath, file_to_check + ".mml"), 'r') as mmlf:
                                mml = mmlf.read()
                            varlist = get_variant_list(mml, sfxmode)
                            potential_files[file_to_check] = (mml, varlist)
                        except IOError:
                            potential_files[file_to_check] = ("", {})
                    if varlist and (variant_to_check in varlist or variant_to_check == ""):
                        variant = variant_to_check
                        found = True
                        break
                    elif file_to_check.count('_') >= 2:
                        file_to_check, _, variant_append = file_to_check.rpartition('_')
                        variant_to_check = variant_append + '_' + variant_to_check
                        if variant_to_check.endswith('_'):
                            variant_to_check = variant_to_check[:-1]
                    else:
                        break
                if found:
                    break
                elif target.count('_') >= 2:
                    target, _, _ = target.rpartition('_')
                elif vid:
                    vid = ""
                    target = vbase
                else:
                    mml, varlist, variant = "", {}, ""
                    break
            if found:
                if "legacy" in searchpath:
                    self[name].is_legacy = True
                break
        
        if not found:
            print(f"warning: in add_random: file not found: {song + '.mml'}")
            return False
            
        self[name].mml = mml
        self[name].file = os.path.join(searchpath, file_to_check)
        self[name].variant = variant if variant else None
        used_song_names.add(song_usage_id(song))
        return True
        
            
def song_usage_id(name):
    if name.count("_") <= 1:
        return name
    return "_".join(name.split("_")[0:2])
        
def song_variant_id(name, idx):
    if name.endswith("_sfx") or name.endswith("_vic"):
        name = name[:-4]
    elif name.endswith("_tr"):
        name = name[:-3]
    if idx == 0x29 or idx == 0x4F or (idx == 0x5D and windy_intro):
        return name, "_sfx"
    elif idx == 0x20:
        return name, "_tr"
    elif idx == 0x2F:
        return name, "_vic"
    else:
        return name, ""
            
def process_music(inrom, meta={}, f_chaos=False, f_battle=True, opera=None, eventmodes=""):
    global used_song_names
    global used_sample_ids
    

    music_pools = {}
    
    # -- load sample configs for normal/legacy
    instmap, legacy_instmap = {}, {}
    sample_parser = configparser.ConfigParser()
    sample_parser.read(os.path.join('tables','brr_samples.txt'))
    for k, v in sample_parser.items("Samples"):
        try:
            instmap[int(k, 16)] = v
        except ValueError:
            print(f"warning: invalid entry {k} in brr_samples.txt")
            
    legacy_parser = configparser.ConfigParser()   
    legacy_parser.read(os.path.join('tables','brr_legacy.txt'))
    for k, v in legacy_parser.items("Samples"):
        try:
            legacy_instmap[int(k, 16)] = v
        except ValueError:
            print(f"warning: invalid entry {k} in brr_legacy.txt")
    
    # -- load random pool configuration for tracks
    try:
        with open(os.path.join('tables','music_ids.txt'), 'r') as f:
            music_id_datamap = f.readlines()
    except IOError:
        print("could not open tables/music_ids.txt, music insertion aborted")
        processing_failed = True
        return 0
        
    for line in music_id_datamap:
        # trim comments
        line = line.split('#')[0]
        # reject blanks and other lines without a xx: ~~ structure
        if ':' not in line: continue
        # finish splitting
        id, line = [s.strip() for s in line.split(':')[:2]]
        name, pool = [s.strip() for s in line.split(',')[:2]]
        # reject bad ids
        if not set(id) <= set("0123456789abcdefABCDEF"):
            print(f"warning: music_ids.txt ({i}): id {id} contains invalid characters")
            continue
        id = int(id, 16)
        if id in song_id_names:
            print(f"warning: music_ids.txt ({i}): multiple definition of id {id:02X}")
            continue
            
        song_id_names[id] = name
        song_name_ids[name] = id
        if pool not in music_pools:
            music_pools[pool] = []
        music_pools[pool].append(name)

    # -- load random choices configuration for pools
    music_choice_map = configparser.ConfigParser()
    music_choice_map.read(os.path.join('custom','music.txt'))
    
    song_pools = {}
    intensitytable = {}
    for pool in music_pools:
        if pool in ["battle", "ext", "fixed", "opera"]:
            continue
        for song in music_choice_map.items(pool):
            valid_slots = [s.strip() for s in song[1].split(',')]
            intense, epic = 0,0
            #holiday stuff
            event_mults = {}
            for s in valid_slots:
                if not s: continue
                if s[0] in eventmodes and ':' not in s:
                    try:
                        event_mults[s[0]] = int(s[1:])
                    except ValueError:
                        print(f"WARNING: in music.txt: could not interpret '{s}'")
            static_mult = 1
            for k, v in event_mults.items():
                static_mult *= v
            #for chaos, we add left side as an option for all entries
            if f_chaos:
                for k, v in music_choice_map.items(pool):
                    if k not in song_pools:
                        song_pools[k] = []
                    song_pools[k].extend([song[0]]*static_mult)
            #parse right side
            for s in valid_slots:
                if not s: continue
                #special entries: holiday multipliers, battle scaling
                if ':' in s and s[0] in eventmodes:
                    s = s.split(':', 1)[1]
                if s[0] == "I":
                    intense = int(s[1:])
                elif s[0] == "E" or s[0] == "G":
                    epic = int(s[1:])
                #for non chaos, we add left side as an option for entries listed on right side
                elif not f_chaos:
                    if "*" in s:
                        slot = s.split('*')
                        mult = int(slot[1])
                        slot = slot[0]
                    else:
                        slot = s
                        mult = 1
                    if slot not in song_pools:
                        song_pools[slot] = []
                    song_pools[slot].extend([song[0]]*mult*static_mult)
            #battle stuffs part2
            intense = max(0, min(intense, 99))
            epic = max(0, min(epic, 99))
            if (intense or epic):
                intensitytable[song[0]] = (intense, epic)
    
    # -- retry loop
    processing_complete = False
    while not processing_complete:
        processing_failed = False

        used_sample_ids = set()
        used_song_names = set()
        
        playlist = Playlist()
                    
        windy_intro = random.choice([True, False, False])
        
        # -- process special cases (battle, opera, tierboss) wrt. choosing tracks
        
        # -- choose tracklist
        for pool, tracks in music_pools.items():
            # fixed pool - does not randomize, loads from data/music/ only
            # TODO - opera is here for now, eventually it should be here only if not using alasdraco
            if pool == "fixed" or pool == "opera":
                for track in tracks:
                    playlist.add_fixed(track)
                continue
            # TODO - battle and ext for now these just auto merge with default
            elif pool == "battle" or pool == "ext":
                continue
            elif pool == "default":
                tracks = tracks + music_pools["battle"] + music_pools["ext"]
            for track in tracks:
                if track not in song_pools:
                    song_pools[track] = []
                ok = playlist.add_random(track, song_pools[track])
                if not ok:
                    processing_failed = True
                    break
        if processing_failed: 
            continue
            
        # -- load tracklist files, while...
        #    - for NON-legacy #WAVE, record used samples in a set
        #    - for legacy #WAVE, convert to #BRR
        for pl_name, pl_entry in playlist.data.items():
            if not pl_entry.mml:
                try:
                    with open(pl_entry.file, "r") as f:
                        pl_entry.mml = f.read()
                except IOError:
                    print(f"file not found: {pl_entry.file}")
                    processing_failed = True
                    break
            sfxmode = True if pl_name in ["ruin", "zozo"] or (pl_name == "assault" and windy_intro) else False
            variant = pl_entry.variant if pl_entry.variant else "_default_"
            # grab inst from mml and turn it into a form we can use
            inst_raw = mml_to_akao(pl_entry.mml, inst_only=True, variant=variant)
            inst = []
            for i, b in enumerate(inst_raw):
                if i % 2:
                    continue
                inst.append(b)
            if pl_entry.is_legacy:
                #legacy: use legacy instmap to make #BRR
                appendix = ""
                for i, id in enumerate(inst):
                    if id > 0:
                        appendix += f"\n#BRR 0x{i+0x20:02X}; ../../../data/samples/{legacy_instmap[id]}\n"
                        #TODO: test if this conflicts with / as variant marker and reconcile somehow
                pl_entry.mml += appendix
            else:
                #non-legacy: record usage so we can determine which samples are needed this seed
                for i in inst:
                    if i > 0:
                        used_sample_ids.add(i)
        if processing_failed:
            continue
            
        # -- process special cases wrt. editing mml content (maybe have to do some of this earlier?)
        #                                                   variant stuff should be figured in add_random
        # TODO
        
        # -- generate virtual sample listfile for insertmfvi
        sample_virtlist = {}
        for id in used_sample_ids:
            sample_virtlist[f"{id:02X}"] = f"{instmap[id]}"
        # -- generate virtual mml listfile for insertmfvi
        mml_virtlist = {}
        for pl_name, pl_entry in playlist.data.items():
            k = song_name_ids[pl_name]
            v = (pl_entry.file, pl_entry.variant, pl_entry.mml)
            mml_virtlist[k] = v
            # while we're at it, record some metadata
            if pl_name not in music_pools["fixed"] and pl_name not in music_pools["opera"]:
                n = os.path.basename(pl_entry.file).split('.')[0]
                print(f"id {k} @ {pl_name} -> name {n}")
                meta[k] = n
            
        # -- run insertmfvi
        outrom = insertmfvi(inrom, virt_sample_list=sample_virtlist, virt_seq_list=mml_virtlist, freespace=JOHNNYDMAD_FREESPACE)
        #outrom = insertmfvi(inrom, virt_sample_list=sample_virtlist, virt_seq_list=None, freespace=JOHNNYDMAD_FREESPACE)
        # -- verify insert worked within parameters (total # samples, size etc)
        #    (will need changes to insertmfvi to get info)
        #    retry ('continue') if bad
        #TODO
        processing_complete = True
        
        # -- we won i think?
    return outrom
        