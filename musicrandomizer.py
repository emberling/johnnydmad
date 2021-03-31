import configparser
import copy
import os
import random
import re

from mml2mfvi import mml_to_akao, get_variant_list
from insertmfvi import insertmfvi, byte_insert, int_insert

JOHNNYDMAD_FREESPACE = ["53C5F-9FDFF", "310000-3FFFFF"]
TRAIN_SAMPLE_ID = 0x3A

SAMPLE_PATH = 'samples'
CUSTOM_MUSIC_PATH = 'custom'
LEGACY_MUSIC_PATH = os.path.join(CUSTOM_MUSIC_PATH, 'legacy')
STATIC_MUSIC_PATH = 'static_music'
PLAYLIST_PATH = 'playlists'
TABLE_PATH = 'tables'
DEFAULT_PLAYLIST_FILE = os.path.join(PLAYLIST_PATH, 'default.txt')
LEGACY_LOADBRR_PATH = "../../samples/"
# For LEGACY_LOADBRR_PATH, note that the filenames from tables/legacy.txt that
#   are appended to this already contain the "legacy/" bit. Path is relative
#   to LEGACY_MUSIC_PATH. OS-specific separators are handled later, '/' is
#   fine here.

used_sample_ids = set()
used_song_names = set()
track_id_names = {}
track_name_ids = {}
    
windy_intro = False
SFXTRACKS = []
APPENDTRACKS = []
LONGTRACKS = []

# Noting some stuff that got confusing because I can't keep my terms straight
# "Playlist" - should refer to the config file determining what songs are used and where.
# "Tracklist" - list of tracks in current seed, with either a song or a pool of potential songs placed in each
# "Track" - aka "song slot", an ID within game files that corresponds to music played in certain situations.
# "Song" - A musical piece loaded from an MML file that will be placed in a track.
# "Category" - A label set in the playlist under which a song is loaded, causing it to randomize into the tracks marked in that category (this is 'pool' atm, but so are other things..)
# "Pool" - The list of available songs for a particular track, or possibly category
#TODO some instances of 'pool' need to be renamed 'category'

class TrackMetadata:
    def __init__(self, title="", album="", composer="", arranged=""):
        self.title, self.album, self.composer, self.arranged = title, album, composer, arranged
        
class TracklistEntry:
    def __init__(self, name):
        self.slotname = name
        self.file = None
        self.mml = None
        self.akao = None
        self.inst = None
        self.variant = None
        self.is_legacy = False
        self.is_fixed = True
        
class Tracklist:
    def __init__(self):
        self.data = {}
        
    def __getitem__(self, key):
        return self.data[key]
        
    def __setitem__(self, key, value):
        self.data[key] = value
        
    def dupe_check(self, name, module="unknown"):
        if name in self.data:
            print(f"warning: in {module}: duplicate tracklist data for {name}, overwriting entry with file {self[name].file}")
            return True
        return False
        
    def add_fixed(self, name):
        self.dupe_check(name, "add_fixed")
        self[name] = TracklistEntry(name)
        self[name].file = os.path.join(STATIC_MUSIC_PATH, name + '.mml')
        used_song_names.add(song_usage_id(name))
        
    def add_random(self, name, pool, idx=None, allow_duplicates=False):
        self.dupe_check(name, "add_random")
        self[name] = TracklistEntry(name)
        self[name].is_fixed = False
        
        if not allow_duplicates:
            pool = [p for p in pool if song_usage_id(p) not in used_song_names]
        if len(pool) < 1:
            print(f"info: pool for {name} is empty, rerolling tracklist")
            input() #debug, #TODO remove
            return False
        song = random.choice(pool)
        
        # check various possible file locations over various possible variants
        if idx is None:
            idx = track_name_ids[name]
        vbase, vsuffix = song_variant_id(song, idx)
        sfxmode = True if name in SFXTRACKS else False
        for searchpath in [CUSTOM_MUSIC_PATH, LEGACY_MUSIC_PATH, STATIC_MUSIC_PATH]:
            target = vbase
            vid = vsuffix
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
                if searchpath == LEGACY_MUSIC_PATH:
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

def init_playlist(fn=DEFAULT_PLAYLIST_FILE):            
    playlist_parser = configparser.ConfigParser()
    playlist_parser.read(fn)
    playlist_map = {}
    for section in playlist_parser:
        for k, v in playlist_parser[section].items():
            if k in playlist_map:
                playlist_map[k] += f", {v}"
            else:
                playlist_map[k] = v
    return playlist_map

def get_jukebox_title(mml, fn):
    n = re.search("(?<=#SHORTNAME )([^;\n]*)", mml, re.IGNORECASE)
    if n:
        n = n.group(0)
    else:
        title = re.search("(?<=#TITLE )([^;\n]*)", mml, re.IGNORECASE)
        title = title.group(0)
        n = os.path.basename(fn).split('.')[0].split('_')[0].upper() + " "
        n += title
        n = n[:18]
    return n
                    
############ variant processing

def apply_variant(mml, type, name="", variant="_default_", check_size=False):
    
    def wind_increment(m):
        val = int(m.group(1))
        if val in [1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14]:
            val += 2
        elif val in [7, 8, 15, 16]: 
            val -= 6
        return "{{{}}}".format(val)
        return m.group(0)

    use_sfxv = False
    append_mml = None
    orig_mml = mml
    
    if type == "rain":
        use_sfxv = True
        append_mml = "append_rain.mml"
    elif type == "wind":
        use_sfxv = True
        append_mml = "append_wind.mml"
        try:
            mml = re.sub("\{[^}']*?([0-9]+)[^}]*?\}", wind_increment, mml)
        except ValueError:
            print("WARNING: failed to add wind sounds ({})".format(name))
    elif type == "train":
        append_mml = "append_train.mml"
        mml = re.sub("\{[^}]*?([0-9]+)[^}]*?\}", "$888\g<1>", mml)
        for i in range(1,9):
            if "$888{}".format(i) not in mml:
                mml = mml + "\n$888{} r;".format(i)
    if append_mml:
        try:
            with open(os.path.join(STATIC_MUSIC_PATH, append_mml), 'r') as f:
                mml += f.read()
        except IOError:
            print("couldn't open {}".format(sfx))
    if check_size:
        if not name:
            name = type
        seq = mml_to_akao(mml, name, use_sfxv, variant=variant)
        if len(seq) > 0x1002:
            mml = orig_mml
    return mml
    
############ tierboss

def generate_tierboss_mml():
    
    # get pool of potential segments (mml files)

    # fail a lot
    attempt = 0
    while attempt < 1000:
        attempt += 1
        
        # pick three
        
        # build sample table
        # retry if n>16
        
        # check sample size
        # retry if n>3746
        
        # grab metadata
        
        # regex fix program changes
        
        # regex & merge segments
        
        # test build akao sequence
        # retry if n>$1002
    return None, None

############ main

def process_music(inrom, meta={}, f_chaos=False, f_battle=True, opera=None, eventmodes=""):
    global used_song_names
    global used_sample_ids
      
    # -- load sample configs for normal/legacy
    instmap, legacy_instmap = {}, {}
    sample_parser = configparser.ConfigParser()
    sample_parser.read(os.path.join(TABLE_PATH,'brr_samples.txt'))
    for k, v in sample_parser.items("Samples"):
        try:
            instmap[int(k, 16)] = v
        except ValueError:
            print(f"warning: invalid entry {k} in brr_samples.txt")
            
    legacy_parser = configparser.ConfigParser()   
    legacy_parser.read(os.path.join(TABLE_PATH,'brr_legacy.txt'))
    for k, v in legacy_parser.items("Samples"):
        try:
            legacy_instmap[int(k, 16)] = v
        except ValueError:
            print(f"warning: invalid entry {k} in brr_legacy.txt")
    
    # -- load map of categories for tracks (i.e. which pool of songs applies to each track)
    try:
        with open(os.path.join(TABLE_PATH,'track_ids.txt'), 'r') as f:
            track_id_map = f.readlines()
    except IOError:
        print(f"could not open {os.path.join(TABLE_PATH,'track_ids.txt')}, music insertion aborted")
        processing_failed = True
        return inrom
        
    category_tracks, track_categories = {}, {}
    for line in track_id_map:
        # trim comments
        line = line.split('#')[0]
        # reject blanks and other lines without a xx: ~~ structure
        if ':' not in line: continue
        # finish splitting
        id, line = [s.strip() for s in line.split(':')[:2]]
        name, category = [s.strip() for s in line.split(',')[:2]]
        # reject bad ids
        if not set(id) <= set("0123456789abcdefABCDEF"):
            print(f"warning: track_ids.txt ({i}): id {id} contains invalid characters")
            continue
        id = int(id, 16)
        if id in track_id_names:
            print(f"warning: track_ids.txt ({i}): multiple definition of id {id:02X}")
            continue
            
        track_id_names[id] = name
        track_name_ids[name] = id
        if category not in category_tracks:
            category_tracks[category] = []
        if category in ["ext"]:
            category = "default"
        category_tracks[category].append(name)
        track_categories[name] = category

    # -- load random choices configuration for categories (playlist file)
    # moved to function for reuse in length test mode
    playlist_map = init_playlist()
    playlist_filename = DEFAULT_PLAYLIST_FILE #TODO
    
    track_pools = {}
    intensitytable = {}
    intensitytable["battle"] = {}
    intensitytable["boss"] = {}
    for song in playlist_map.items():
        valid_trackslots = [s.strip() for s in song[1].split(',')]
        intense, epic = 0,0
        song_categories = set()
        #holiday stuff
        event_mults = {}
        for s in valid_trackslots:
            if not s: continue
            if s[0] in eventmodes and ':' not in s:
                try:
                    event_mults[s[0]] = int(s[1:])
                except ValueError:
                    print(f"WARNING: in playlist {playlist_filename}: could not interpret '{s}'")
        static_mult = 1
        for k, v in event_mults.items():
            static_mult *= v
        #parse right side
        for s in valid_trackslots:
            if not s: continue
            #special entries: holiday multipliers, battle scaling
            if ':' in s and s[0] in eventmodes:
                s = s.split(':', 1)[1]
            if s[0] == "I":
                intense = int(s[1:])
            elif s[0] == "E" or s[0] == "G":
                epic = int(s[1:])
            #for all modes, link left side to the category containing each right side entry
            #for non chaos, we add left side as an option for entries listed on right side
            else:
                if "*" in s:
                    trackslot = s.split('*')
                    mult = int(trackslot[1])
                    trackslot = trackslot[0]
                else:
                    trackslot = s
                    mult = 1
                if trackslot in track_categories:
                    # quietly do nothing for unknown tracknames
                    category = track_categories[trackslot]
                    song_categories.add(category)
                if trackslot not in track_pools:
                    track_pools[trackslot] = []
                if not f_chaos:
                    track_pools[trackslot].extend([song[0]]*mult*static_mult)
        #for chaos, we add left side as an option for all entries
        if f_chaos:
            if not song_categories:
                # If a song has no valid non-chaos tracks, put it in chaos default
                song_categories.add("default")
            for category in song_categories:
                for trackslot in category_tracks[category]:
                    if trackslot not in track_pools:
                        track_pools[trackslot] = []
                    track_pools[trackslot].extend([song[0]]*static_mult)
        #battle stuffs part2
        intense = max(0, min(intense, 99))
        epic = max(0, min(epic, 99))
        if "boss" in song_categories:
            intensitytable["boss"][song[0]] = intense
        if "battle" in song_categories:
            intensitytable["battle"][song[0]] = epic
    
    # -- retry loop
    processing_complete = False
    attempts = 0
    while not processing_complete:
        processing_failed = False

        used_sample_ids = set()
        used_song_names = set()
        
        tracklist = Tracklist()
                    
        LONGTRACKS = ["ending1", "ending2"]
        SFXTRACKS = ["ruin", "zozo"]
        windy_intro = random.choice([True, False, False])
        if windy_intro:
            SFXTRACKS.append("assault")
        APPENDTRACKS = SFXTRACKS + ["train"]
            
        if attempts >= 1000:
            print("Music randomization failed after 1000 attempts. Your custom music configuration files and/or filters may be too restrictive.")
            return inrom
        attempts += 1
        
        # -- process special cases (battle, opera, tierboss) wrt. choosing tracks
        
        # tierboss
        # processing tierboss first to avoid having to check for used song names
        tierboss_mml, tierboss_metadata = generate_tierboss_mml()
        # TODO add tierboss_metadata entries to used_song_names
        
        # battle
        progression = {}
        already_added = set()
        progression['battle'] = ["battle", "bat2", "bat3", "bat4"]
        progression['boss'] = ["mboss", "boss", "atma", "dmad5"]
        for cat, order in progression.items():
            prog_attempts = 0
            while prog_attempts < 1000:
                prog_choices = []
                prog_level = 0
                temp_used_song_names = copy.copy(used_song_names)
                for track in order:
                    # get song options for tier (exclude by used and under level)
                    if track not in track_pools:
                        prog_attempts = 1000
                        break
                    track_pool = [s for s in track_pools[track] if s not in temp_used_song_names and s not in already_added and intensitytable[cat][s] >= prog_level]
                    # choose one, if no options retry
                    if not track_pool:
                        prog_attempts += 1
                        continue
                    choice = random.choice(track_pool)
                    prog_level = intensitytable[cat][choice]
                    prog_choices.append(choice)
                    temp_used_song_names.add(choice)
                    print(f"prog: {track} - chose {choice} at intensity {prog_level} from pool {track_pool}")
                if len(prog_choices) == len(order):
                    break
            # add to tracklist
            for i, choice in enumerate(prog_choices):
                ok = tracklist.add_random(progression[cat][i], [choice])
                if not ok:
                    processing_failed = True
                    break
                already_added.add(progression[cat][i])
            if processing_failed:
                break
        if processing_failed: 
            continue
        
        # -- choose tracklist
        for category, tracks in sorted(category_tracks.items()):
            # fixed category - does not randomize, loads from static_music/ only
            # TODO - opera is here for now, eventually it should be here only if not using alasdraco
            if category == "fixed" or category == "opera":
                for track in tracks:
                    tracklist.add_fixed(track)
                continue
            # 'ext' uses default's pool, it's just a marker to allow excluding those tracks
            elif category == "ext":
                continue
            elif category == "default":
                tracks = tracks + category_tracks["ext"]
            if tracks: #make deterministic based on seed, don't let any undefined order (from dict) sneak in
                tracks = sorted(tracks)
                random.shuffle(tracks)
            for track in tracks:
                if track in already_added:
                    continue
                if track not in track_pools:
                    track_pools[track] = []
                ok = tracklist.add_random(track, track_pools[track])
                if not ok:
                    processing_failed = True
                    break
        if processing_failed: 
            continue
            
        # -- load tracklist files, while...
        #    - for NON-legacy #WAVE, record used samples in a set
        #    - for legacy #WAVE, convert to #BRR
        for tl_name, tl_entry in tracklist.data.items():
            if not tl_entry.mml:
                try:
                    with open(tl_entry.file, "r") as f:
                        tl_entry.mml = f.read()
                except IOError:
                    print(f"file not found: {tl_entry.file}")
                    processing_failed = True
                    break
            variant = tl_entry.variant if tl_entry.variant else "_default_"
            # grab inst from mml and turn it into a form we can use
            inst_raw = mml_to_akao(tl_entry.mml, inst_only=True, variant=variant)
            inst = []
            for i, b in enumerate(inst_raw):
                if i % 2:
                    continue
                inst.append(b)
            if tl_entry.is_legacy:
                #legacy: use legacy instmap to make #BRR
                appendix = ""
                for i, id in enumerate(inst):
                    if id > 0:
                        appendix += f"\n#BRR 0x{i+0x20:02X}; {os.path.join(LEGACY_LOADBRR_PATH, legacy_instmap[id])}\n"
                        #TODO: test if this conflicts with / as variant marker and reconcile somehow
                tl_entry.mml += appendix
            else:
                #non-legacy: record usage so we can determine which samples are needed this seed
                for i in inst:
                    if i > 0:
                        used_sample_ids.add(i)
            if tl_name in APPENDTRACKS:
                append_type_map = {
                    "train":   "train",
                    "ruin":    "wind",
                    "assault": "wind",
                    "zozo":    "rain"}
                tl_entry.mml = apply_variant(tl_entry.mml, append_type_map[tl_name], name=tl_entry.file, variant=variant, check_size = True if tl_name == "assault" else False)
                if append_type_map[tl_name] == "train":
                    used_sample_ids.add(TRAIN_SAMPLE_ID)
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
        for tl_name, tl_entry in tracklist.data.items():
            k = track_name_ids[tl_name]
            is_sfx = True if tl_name in SFXTRACKS else False
            is_long = True if tl_name in LONGTRACKS else False
            v = (tl_entry.file, tl_entry.variant, is_sfx, is_long, tl_entry.mml)
            mml_virtlist[k] = v
            
            # while we're at it, record some metadata
            title = re.search("(?<=#TITLE )([^;\n]*)", tl_entry.mml, re.IGNORECASE)
            album = re.search("(?<=#ALBUM )([^;\n]*)", tl_entry.mml, re.IGNORECASE)
            composer = re.search("(?<=#COMPOSER )([^;\n]*)", tl_entry.mml, re.IGNORECASE)
            arranged = re.search("(?<=#ARRANGED )([^;\n]*)", tl_entry.mml, re.IGNORECASE)
            title = title.group(0) if title else "??"
            album = album.group(0) if album else "??"
            composer = composer.group(0) if composer else "??"
            arranged = arranged.group(0) if arranged else "??"
            
            # Jukebox title
            if tl_name not in category_tracks["fixed"] and tl_name not in category_tracks["opera"]:
                meta[k] = get_jukebox_title(tl_entry.mml, tl_entry.file)
            #metadata[k] = TrackMetadata(title, album, composer, arranged, menuname)

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
        
#########################################

def process_formation_music_by_table(data, form_music_overrides={}):
    
    o_forms = 0xF6200
    o_formaux = 0xF5900
    o_monsters = 0xF0000
    o_epacks = 0xF5000
    
    with open(os.path.join(TABLE_PATH,"formationmusic.txt"), "r") as f:
        tbl = f.readlines()
    
    table = []
    for line in tbl:
        line = [s.strip() for s in line.split()]
        if len(line) == 2: line.append(None)
        if len(line) == 3: table.append(line)
    
    event_formations = set()
    for i in range(0,256):
        loc = o_epacks + i*4
        event_formations.add(int.from_bytes(data[loc:loc+2], "little"))
        event_formations.add(int.from_bytes(data[loc+2:loc+4], "little"))
    
    for line in table:
        #table format: [formation id] [music bitfield] [force music on/off]
        #value of 'c' forces music on if:
        #   unrunnable enemy in formation
        #   hard to run enemy in formation
        #   "attack first" enemy in formation
        #   formation is present in packs > 255 (event battles)
        try:
            fid = int(line[0])
        except ValueError:
            continue
        
        # account for random music settings in other parts of the randomizer
        # ancient cave bosses can be set to 5, 2, or 4
        # superbosses (formations_hidden) can be set to anything 1-5
        # I don't recommend using random tierboss in this way; it should only be used on the tierboss itself. So we need to adjust these settings
        # 1 (boss) remains 1
        # 2 (superboss) changes to 6 (battle4)
        # 3 (savethem) changes to 5 (battle3)
        # 4 (returners) changes to 7 (event)
        # 5 (dmad1) changes to 2 (superboss)
        force_music = False
        if fid in form_music_overrides:
            mutation_table = [0, 1, 6, 5, 7, 2, 0, 0]
            line[1] = mutation_table[form_music_overrides[fid]]
            force_music = True
            
        try:
            mbf = int(line[1]) << 3
        except ValueError:
            mbf = 0
        pos = o_formaux + fid*4
        dat = bytearray(data[pos:pos+4])
        
        dat[3] = (dat[3] & 0b11000111) | mbf
        if line[2] == "0":
            dat[1] = dat[1] | 0b00000010
            dat[3] = dat[3] | 0b10000000
        elif line[2] == "c":
            if fid in event_formations:
                force_music = True
            else:
                for m in range(0,6):
                    fpos = o_forms + fid*15
                    if (data[fpos+1] >> m) & 1:
                        mid = data[fpos+2+m] + (((data[fpos+14] >> m) & 1) << 8)
                        mb = data[o_monsters+mid*32+19]
                        if mb & 0b00001011:
                            force_music = True
                            break
        if line[2] == "1" or force_music:
            dat[1] = dat[1] & 0b11111101
            dat[3] = dat[3] & 0b01111111
        data = byte_insert(data, pos, dat)
    
        #update relevant tables in program code:
        # IDs of songs that pause/resume current song when played: change to battle1-4 and mboss
        data = byte_insert(data, 0x506F9, b"\x24\x5E\x5F\x60\x61")
        # formation battle music table: battle, boss1, boss2, battle2, battle3, dmad123, battle4, mboss
        data = byte_insert(data, 0x2BF3B, b"\x24\x14\x33\x5E\x5F\x3B\x60\x61")
        
    return data
    
def process_map_music(data):
    #find range of valid track #s
    songcount_byte = 0x53C5E
    max_bgmid = data[songcount_byte]
    max_bgmid -= 4 #extra battles always go last
    
    map_offset = 0x2D8F00
    map_block_size = 0x21
    map_music_byte = 0x1C
    
    #replace track ids in map data
    replacements = {}
    replacements[0x51] = [ #Phantom Forest (forest)
        0x84, 0x85, 0x86, 0x87
        ]
    replacements[0x55] = [ #Daryl's Tomb (tomb)
        0x129, 0x12A, 0x12B, 0x12C
        ]
    replacements[0x56] = [ #Cyan's Dream (dream)
        0x13D, #stoogeland
        0x13F, 0x140 #dream of a mine
        ]
    replacements[0x57] = [ #Ancient Castle (ancient)
        0x191, 0x192, #cave
        0x196, 0x197, 0x198 #ruins
        ]
    replacements[0x58] = [ #Phoenix Cave (phoenix)
        0x139, 0x13B
        ]
    replacements[0x59] = [ #Sealed Gate Cave (gate)
        0x17E, 0x17F, 0x180, 0x181, 0x182
        ]
    replacements[0x5A] = [ #Mt. Zozo (mount2)
        0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5
        ]
    replacements[0x5B] = [ #Figaro Engine Room (engine)
        0x3E, 0x3F, 0x40, 0x41, 0x42
        ]
    replacements[0x5C] = [ #Village (village)
        0x0E, 0x0F, 0x10, #chocobo stable
        0x5D, 0x5E, #Sabin's house
        0x9D, 0xA0, 0xA1, 0xA4, #Mobliz (WoB)
        0xBC #Kohlingen (WoB)
        ]
    replacements[0x5D] = [ #Opening magitek sequence (assault)
        0x13, #outside south
        0x27, #outside north
        0x2A #Tritoch mine room
        ]
    replacements[0x00] = [ #Change maps to "continue current music"
        0x29 #Narshe mines 1
        ]
        
    for bgm_id, maps in replacements.items():
        if bgm_id > max_bgmid: continue
        for map_id in maps:
            offset = map_offset + (map_id * map_block_size) + map_music_byte
            data = byte_insert(data, offset, bytes([bgm_id]))
            
    #also replace relevant play song events
    def adjust_event(dat, offset, oldid, newid):
        op_lengths = {}
        for o in [0x38, 0x39, 0x3A, 0x3B, 0x45, 0x47, 0x49, 0x4A, 0x4E, 0x4F, 0x54, 0x5B, 0x5C, 0x7B, 0x82, 0x8E, 0x8F, 0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x9A, 0x9D, 0xA2, 0xA6, 0xA8, 0xA9, 0xAA, 0xAB, 0xAC, 0xAD, 0xAE, 0xAF, 0xB1, 0xBB, 0xBF, 0xDE, 0xDF, 0xE0, 0xE1, 0xE2, 0xE3, 0xE4, 0xF7, 0xF8, 0xFA, 0xFD, 0xFE]:
            op_lengths[o] = 1
        for o in [0x35, 0x36, 0x37, 0x3D, 0x3E, 0x41, 0x42, 0x46, 0x50, 0x52, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x62, 0x63, 0x77, 0x78, 0x6C, 0x7D, 0x80, 0x81, 0x86, 0x87, 0x8D, 0x98, 0x9B, 0x9C, 0xA1, 0xA7, 0xB0, 0xB4, 0xB5, 0xB8, 0xB9, 0xBA, 0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0xDA, 0xDB, 0xDC, 0xDD, 0xE7, 0xF0, 0xF2, 0xF3, 0xF4, 0xF9]:
            op_lengths[o] = 2
        for o in [0x37, 0x3F, 0x40, 0x43, 0x44, 0x48, 0x4B, 0x4C, 0x4D, 0x5D, 0x5E, 0x5F, 0x60, 0x64, 0x65, 0x70, 0x71, 0x72, 0x7E, 0x7F, 0x84, 0x85, 0x8B, 0x8C, 0xBC, 0xEF, 0xF1]:
            op_lengths[o] = 3
        for o in [0x51, 0x53, 0x61, 0x79, 0x88, 0x89, 0x8A, 0x99, 0xB2, 0xBD, 0xE8, 0xE9, 0xEA, 0xEB, 0xF5, 0xF6]:
            op_lengths[o] = 4
        for o in [0x3C, 0x7A, 0xB3, 0xB7]:
            op_lengths[o] = 5
        for o in [0x6A, 0x6B, 0x6C, 0xA0, 0xC0, 0xC8]:
            op_lengths[o] = 6
        for o in [0xC1, 0xC9]:
            op_lengths[o] = 8
        for o in [0xC2, 0xCA]:
            op_lengths[o] = 10
        for o in [0xC3, 0xCB]:
            op_lengths[o] = 12
        for o in [0xC4, 0xCC]:
            op_lengths[o] = 14
        for o in [0xC5, 0xCD]:
            op_lengths[o] = 16
        for o in [0xC6, 0xCE]:
            op_lengths[o] = 17
        for o in [0xC7, 0xCF]:
            op_lengths[o] = 18
        
        changes = []
        loc = offset
        while True:
            op = dat[loc]
            #print(f"${loc:06X}: {op:02X}")
            if op == 0xFE:
                break
            elif op in range(0, 0x34): #action queue
                loc += 2 + (dat[loc+1] & 0x7F)
            elif op in [0x73, 0x74]: #bitmap
                loc += 3 + dat[loc+2] * dat[loc+3]
            elif op == 0xB6: #variable length dialogue choice
                loc += 1
                while dat[loc] != 0xFE and edat[loc+2] <= 2:
                    loc += 3
            elif op == 0xBE: #variable length switch/case
                loc += 1 + dat[loc+1]*3
            elif op == 0xF0: #play song
                if dat[loc+1] == oldid:
                    changes.append((loc+1, newid))
                loc += 2
            elif op == 0xF1: #play song with fade
                if dat[loc+1] == oldid:
                    changes.append((loc+1, newid))
                loc += 3
            elif op in op_lengths:
                loc += op_lengths[op]
            else:
                print("unexpected event op ${:02X} at ${:06X}".format(op, loc))
                break
                
        #print("full event at ${:06X}:".format(offset))
        #for b in range(offset, loc):
        #    print("{:02X} ".format(dat[b]), end="")
        #print()
        
        for ch in changes:
            #print("at ${:06X}: {:02X} {:02X} -> {:02X}".format(ch[0]-1, dat[ch[0]-1], dat[ch[0]], ch[1]))
            dat = byte_insert(dat, ch[0], bytes([ch[1]]))
       
        return dat
        
    def adjust_entrance_event(dat, mapid, oldid, newid):
        event_offset = 0x0A0000
        entrance_table = 0x11FA00
        table_offset = entrance_table + mapid*3
        event_offset += dat[table_offset]
        event_offset += (dat[table_offset+1] << 8)
        event_offset += (dat[table_offset+2] << 16)
        dat = adjust_event(dat, event_offset, oldid, newid)
        return dat
        
    data = adjust_entrance_event(data, 0xA2, 0x2A, 0x5C) #mobliz
    data = adjust_entrance_event(data, 0xC0, 0x2A, 0x5C) #kohlingen
    data = adjust_event(data, 0xC3B0E, 0x2A, 0x5C) #kohlingen, WoR, locke recruited
    
    data = adjust_event(data, 0xC9A4F, 0x39, 0x5D) #opening mission
    
    # add music conditional event for Narshe Mines 1 map
    event = b"\xC0\x01\x80\x5A\x39\x02" #if you've met arvis, jump to "play Narshe music"
    event += b"\xB2\x01\x9B\x02" #subroutine: put terra, biggs, wedge on magitek armor
    event += b"\xF0\x5D\xFE" #play opening mission track & return
    data = byte_insert(data, 0xC9F1A, event)
    # 3 bytes unused, C9F27 - C9F29
    
    #code from Mines 1 entrance event moved to subroutine
    #Replaces Save Point tutorial event (already dummied out by BC)
    event = b"\x44\x00\xC0\x44\x0E\xC0\x44\x0F\xC0\xFE" #Put terra, biggs, wedge on magitek armor
    data = byte_insert(data, 0xC9B01, event)
    # $12 bytes unused, C9B0B - C9B1C
    
    data = byte_insert(data, 0xC9F1D, b"\x5A\x39\x02")
    
    return data