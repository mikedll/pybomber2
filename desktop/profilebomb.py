#!/usr/bin/python2.3

import bomberman

PROFILEFILE="Profile.tmp"

def hotshotProfile():
    print "using hotshot"
    import hotshot
    prof = hotshot.Profile(PROFILEFILE)
    prof.runcall(bomberman.main)
    prof.close()

def profileProfile():
    print "using standard profiler"
    import profile
    profile.run('bomberman.main()', PROFILEFILE)

def process(filename):
    import pstats
    try:
        p = pstats.Stats(filename)
        p.sort_stats('time', 'calls').print_stats(60)
    except:
        print "error processing"
        try: 
            import hotshot
            stats = hotshot.stats.load(PROFILEFILE)
            stats.strip_dirs()
            stats.sort_stats('time', 'calls')
            stats.print_stats(60)
        except:
            print "error processing"

def main():
    import sys
    if "hotshot" in sys.argv:
        try:
            hotshotProfile()
        except:
            print "caught exception in hotshotProfile"
    elif "process" in sys.argv:
        process(PROFILEFILE)
        sys.exit()
    else:
        profileProfile()
    process(PROFILEFILE)

if __name__ == "__main__":
    main()

