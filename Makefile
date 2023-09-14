README.md: footer.md plugins/modules/perlmod_install_info.py
	rm -f $@.tmp*
	ansible-doc -M plugins/modules -t module --json perlmod_install_info > \
	  $@.tmp1
	pipenv run dev/ansible-doc-to-markdown.py $@.tmp1 > $@.tmp2
	rm -f $@.tmp1
	cat footer.md >> $@.tmp2
	mv $@.tmp2 $@
