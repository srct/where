import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
    selector: 'app-search',
    templateUrl: './search.component.html',
    styleUrls: ['./search.component.scss']
})
export class SearchComponent {
    form: FormGroup;

    // TODO: Make dynamic
    autocompleteOptions: string[] = ['Water Fountain', 'Johnson Center'];

    constructor(fb: FormBuilder) {
        this.form = fb.group({
            search: ''
        });

        // TODO: Actually do stuff when user searches
    }
}
