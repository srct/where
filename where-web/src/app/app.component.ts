import { Component, ChangeDetectionStrategy, ChangeDetectorRef, OnDestroy } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppComponent implements OnDestroy {
    private mobileQuery: MediaQueryList;
    private mobileQueryListener;

    constructor(cd: ChangeDetectorRef, media: MediaMatcher) {
        this.mobileQuery = media.matchMedia('(max-width: 600px)');

        this.mobileQueryListener = () => cd.detectChanges();

        this.mobileQuery.addListener(this.mobileQueryListener);
    }

    get isMobile(): boolean {
        return this.mobileQuery.matches;
    }

    ngOnDestroy() {
        this.mobileQuery.removeListener(this.mobileQueryListener);
    }
}
