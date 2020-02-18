import { Component } from '@angular/core';
import { latLng, tileLayer } from 'leaflet';

@Component({
    selector: 'app-map',
    templateUrl: './map.component.html',
    styleUrls: ['./map.component.scss']
})
export class MapComponent {
    options = {
        layers: [
            tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '...' })
        ],
        zoom: 17,
        center: latLng(38.831493, -77.311485)
    };
}
