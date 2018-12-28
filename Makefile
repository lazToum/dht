PREFIX = /usr/local

all:
	sed "s|%PREFIX%|$(PREFIX)|g" dht.service.in > dht.service
	sed "s|PREFIX|$(PREFIX)|g" dht.py > dht
	@echo "Modify as needed the dht.env file"
	@echo "After install you can modify $(PREFIX)/dht.env"

clean:
	rm -f dht
	rm -f dht.service

install: all
	python3 -m pip install -r requirements.txt
	install -D dht.env $(DESTDIR)$(PREFIX)/share/dht.env
	chmod +x dht
	install -D dht $(DESTDIR)$(PREFIX)/bin/dht
	install -D -m 644 dht.service $(DESTDIR)/usr/lib/systemd/system/dht.service
	systemctl daemon-reload
	@echo "use: systemctl start|stop|status|enable|disable dht.service"
	@echo "or just /usr/local/bin/dht"
uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/dht
	rm -f $(DESTDIR)/usr/lib/systemd/system/dht.service
	rm -f $(DESTDIR)$(PREFIX)/share/dht.env
