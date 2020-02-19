import { Component, ChangeDetectorRef, OnDestroy, ChangeDetectionStrategy } from '@angular/core';
import { latLng, tileLayer, MapOptions, TileLayer } from 'leaflet';
import { MediaMatcher } from '@angular/cdk/layout';

const createLayer = (map) => tileLayer(
    map,
    {
        attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19
    }
);

const LIGHT_MODE_LAYER = createLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png');
const DARK_MODE_LAYER = createLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png');

@Component({
    selector: 'app-map',
    templateUrl: './map.component.html',
    styleUrls: ['./map.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class MapComponent implements OnDestroy {

    mapOptions: MapOptions = {
            zoom: 17,
            center: latLng(38.831493, -77.311485)
    };

    private darkModeQuery: MediaQueryList;
    private darkModeQueryListener;

    constructor(private cd: ChangeDetectorRef, media: MediaMatcher)  {
        this.darkModeQuery = media.matchMedia('(prefers-color-scheme: dark)');

        this.darkModeQueryListener = () => cd.detectChanges();

        this.darkModeQuery.addListener(this.darkModeQueryListener);
    }

    get isDarkMode(): boolean {
        return this.darkModeQuery.matches;
    }

    get mapLayers(): TileLayer[] {
        return this.isDarkMode ? [DARK_MODE_LAYER] : [LIGHT_MODE_LAYER];
    }

    ngOnDestroy() {
        this.darkModeQuery.removeListener(this.darkModeQueryListener);
    }
}
