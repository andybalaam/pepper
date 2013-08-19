
# TODO: Don't need perl to strip newlines!
all:
	pepper painter.pepper | perl -pe "s/\n//" - > tmp.svg && display tmp.svg
	rm tmp.svg

