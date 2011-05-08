"""
This crazy script has cleansed my iTunes library quite a bit. It
looks at the track and artist name looking for the common
'featuring' strings like the following:

Featuring
ft.
feat
f.

It takes this info and then sticks it in the comment.

Some rap track (f. Q-Tip)

turns into a string in the comment like this:

(Featuring Q-Tip)

The script only processes the current selection in iTunes. And it
only writes to the files if the '-r' option is used.

Written by Clayton Parker (claytron)
"""
import re
from csv import DictWriter
from optparse import OptionParser
from appscript import app


def main():
    """move (featuring Rahzel) info out of track/artist names
    """
    version = "1.0"
    description = """\
This script will allow you to modify the tracks in your iTunes database.
Select the items that you want to modify in iTunes, then run this
script from the command line using the options below. The "featuring"
strings will be normalized and added to the comment tag as (Featuring
Some Artist). The previous contents of the comment will be left intact.
"""
    parser = OptionParser(version=version, description=description)
    # always default to a 'dry run'
    parser.add_option(
        "-r", "--real-run",
        dest="real_run", action="store_true",
        help="Change the iTunes database (default: False)",
        default=False)
    parser.add_option(
        "-c", "--with-csv",
        dest="with_csv", action="store_true",
        help="Write change info into a CSV file",
        default=False)
    parser.add_option(
        "-w", "--featuring-with",
        dest="featuring_with", action="store_true",
        help="Take care of 'with'",
        default=False)
    parser.add_option(
        "-n", "--no-parens",
        dest="no_parens", action="store_true",
        help="""\
Process the tracks without parenthesis (be CAREFUL with this option,
since "featuring" is a common word)
""",
        default=False)
    (options, args) = parser.parse_args()

    real_run = options.real_run
    featuring_with = options.featuring_with
    no_parens = options.no_parens

    if featuring_with and no_parens:
        parser.error(
            "'Featuring with' and 'No Parens' cannot be used together")

    if options.with_csv:
        # set up a csv file to keep track of all the info changes
        csv_file = open('name_change.csv', 'w')
        fieldnames = [
            'Artist',
            'Album',
            'orig_name',
            'new_name',
            'new_artist',
            'orig_comment',
            'new_comment',
        ]
        # set up our csv writer
        csv_writer = DictWriter(csv_file, fieldnames)
        write = csv_writer.writerow
        # write the header row
        header_row = dict([(f, f) for f in fieldnames])
        write(header_row)

    # Featuring string regex (f. ft. feat. feat with and featuring)
    #                     or [f. ft. feat. feat with and featuring]
    # TODO this does not take care of this case:
    #      Song name (Featuring Artist) (remix)
    #
    #      Also, the trailing ) is not included in the group (see the silly
    #      adding of the ')' below)
    if featuring_with:
        # same as the base, but added 'With'
        # This is a common word and can be conflicting
        feat = re.compile(
            r"([\[(](?:ft?\.|with|featuring|feat(?:[\.]|))(.*)[\])])", re.I)
    elif no_parens:
        # this takes care of featuring that do not have parenthesis
        # CAVEAT: this won't do 'featuring' since that's a common word
        #         also doesn't do 'feat' but does handle "feat."
        #         also doesn't do 'with' for the same reasons
        feat = re.compile(r"([^(]f(?:ea)?t?\.(.+))", re.I)
    else:
        feat = re.compile(
            r"([\[(](?:ft?\.|featuring|feat(?:[\.]|))(.*)[\])])", re.I)

    it = app('iTunes')
    current_selection = it.selection()
    for track in current_selection:
        track_dict = {}
        track_name = track.name()
        track_dict['orig_name'] = track_name.encode('utf-8')
        track_comment = track.comment()
        track_dict['orig_comment'] = track_comment.encode('utf-8')
        artist_name = track.artist()
        track_dict['Artist'] = track.artist().encode('utf-8')
        track_dict['Album'] = track.album().encode('utf-8')
        ft_track = re.search(feat, track_name)
        ft_artist = re.search(feat, artist_name)
        # if (Featuring) in artist or track name
        if ft_track is not None or ft_artist is not None:
            # take care of the track name
            if ft_track is not None:
                res = ft_track.groups()
                feat_string = res[0]
                new_name = track_name.replace(feat_string, '').strip()
                if real_run:
                    track.name.set(new_name)
                track_dict['new_name'] = new_name.encode('utf-8')
                feat_artists = res[1]
                feat_artists_string = u"(Featuring %s)" % feat_artists.strip()
            # take care of the artist name
            if ft_artist is not None:
                res = ft_artist.groups()
                feat_string = res[0]
                new_name = artist_name.replace(feat_string, '').strip()
                if real_run:
                    track.artist.set(new_name)
                track_dict['new_artist'] = new_name.encode('utf-8')
                feat_artists = res[1]
                feat_artists_string = u"(Featuring %s)" % feat_artists.strip()

            # if the comment has more than an empty string...
            if track_comment:
                ft_comment = re.search(feat, track_comment)
                # check for the (Feat. Artist) already in the comment
                if ft_comment is not None:
                    res = ft_comment.groups()
                    feat_string = res[0]
                    track_comment = track_comment.replace(feat_string, '')
                    track_comment = track_comment.strip()
                # set up the string as we wish
                feat_artists_string = u"\n\n%s" % feat_artists_string
            new_comment = track_comment + feat_artists_string
            if real_run:
                track.comment.set(new_comment)
            track_dict['new_comment'] = new_comment.encode('utf-8')
            if options.with_csv:
                write(track_dict)
    # close out the csv file
    if options.with_csv:
        csv_file.close()

if __name__ == '__main__':
    main()
