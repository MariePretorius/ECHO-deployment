
import { Component, Output, EventEmitter } from '@angular/core';
import { ThemeService } from './../../services/theme.service';
import { CommonModule } from '@angular/common';
import { SvgIconComponent } from '../svg-icon/svg-icon.component';
import { Router } from '@angular/router';
import { ScreenSizeService } from '../../services/screen-size-service.service';

@Component({
    selector: 'app-navbar',
    standalone: true,
    imports: [CommonModule, SvgIconComponent],
    templateUrl: './navbar.component.html',
    styleUrl: './navbar.component.css',
})
export class NavbarComponent {
    constructor(
        public themeService: ThemeService,
        private router: Router,
        private screenSizeService: ScreenSizeService
    ) {}
    screenSize?: string;
    currentSelection: string = 'All';

    ngOnInit() {
        this.screenSizeService.screenSize$.subscribe(screenSize => {
          this.screenSize = screenSize;
        });
    }

    homeSvg: string =
        'M2.5447 22.1725L2.4997 22.2225H7.49976V47.2222C7.49976 47.959 7.76316 48.6655 8.23201 49.1864C8.70085 49.7073 9.33675 50 9.9998 50H40.0002C40.6633 50 41.2991 49.7073 41.768 49.1864C42.2368 48.6655 42.5002 47.959 42.5002 47.2222V22.2225H47.5003L47.4553 22.1725C47.8708 22.1899 48.2835 22.0903 48.6551 21.883C49.0266 21.6756 49.3449 21.3671 49.5803 20.9864C49.7625 20.6827 49.889 20.3422 49.9526 19.9842C50.0163 19.6262 50.0158 19.2578 49.9512 18.9C49.8867 18.5422 49.7593 18.2021 49.5765 17.899C49.3936 17.5959 49.1587 17.3358 48.8853 17.1336L26.385 0.467079C25.9742 0.162528 25.4914 0 24.9975 0C24.5036 0 24.0208 0.162528 23.61 0.467079L14.9999 6.84758V2.77817C14.9999 2.04146 14.7365 1.33493 14.2676 0.814001C13.7988 0.293071 13.1629 0.000415905 12.4998 0.000415905C11.8368 0.000415905 11.2009 0.293071 10.732 0.814001C10.2632 1.33493 9.9998 2.04146 9.9998 2.77817V10.5559L1.11468 17.1336C0.841292 17.3358 0.606443 17.5959 0.423548 17.899C0.240653 18.2021 0.113295 18.5422 0.0487529 18.9C-0.0157894 19.2578 -0.016252 19.6262 0.0473909 19.9842C0.111034 20.3422 0.237535 20.6827 0.419668 20.9864C0.654598 21.3677 0.972795 21.6766 1.34446 21.884C1.71612 22.0915 2.1291 22.1907 2.5447 22.1725ZM30.0001 44.4445H19.9999V36.1112C19.9999 35.3745 20.2633 34.668 20.7322 34.1471C21.201 33.6261 21.8369 33.3335 22.5 33.3335H27.5C28.1631 33.3335 28.799 33.6261 29.2678 34.1471C29.7367 34.668 30.0001 35.3745 30.0001 36.1112V44.4445ZM19.9999 22.2225H30.0001C30.6631 22.2225 31.299 22.5151 31.7679 23.036C32.2367 23.557 32.5001 24.2635 32.5001 25.0002C32.5001 25.7369 32.2367 26.4434 31.7679 26.9644C31.299 27.4853 30.6631 27.778 30.0001 27.778H19.9999C19.3369 27.778 18.701 27.4853 18.2321 26.9644C17.7633 26.4434 17.4999 25.7369 17.4999 25.0002C17.4999 24.2635 17.7633 23.557 18.2321 23.036C18.701 22.5151 19.3369 22.2225 19.9999 22.2225Z'; // SVG path for selected theme

    selectedSvg: string = this.homeSvg;
    otherSvg1: string =
        'M27.2 0H34V51H27.2V0ZM13.6 12.75V51H20.4V12.75H13.6ZM6.8 25.5H0V51H6.8V25.5Z';
    otherSvg2: string =
        'M8.63935 0H26.3578C27.3436 0 28.1483 1.09766 28.1483 2.43359V4.96094H6.84883V2.43359C6.84883 1.09375 7.65356 0 8.63935 0ZM3.22754 14.9922H31.7725C33.5486 14.9922 35 16.9648 35 19.3789V43.6133C35 46.0273 33.5486 48 31.7725 48H3.22754C1.45139 48 0 46.0273 0 43.6133V19.3789C0 16.9648 1.45139 14.9922 3.22754 14.9922ZM15.5514 22.8047L23.3946 30.2383C23.524 30.3516 23.6418 30.5 23.7338 30.6797C24.1017 31.4023 23.9666 32.3945 23.4349 32.8945L15.6261 40.2344C15.4249 40.4609 15.1663 40.5937 14.8818 40.5937C14.2322 40.5937 13.7063 39.8789 13.7063 38.9961V24.1094H13.712C13.712 23.793 13.781 23.4766 13.9218 23.1992C14.2926 22.4766 15.0226 22.3008 15.5514 22.8047ZM5.2135 7.34766H29.7836C30.7694 7.34766 31.5742 8.44531 31.5742 9.78125V12.4063H3.42298V9.78125C3.42298 8.44141 4.22771 7.34766 5.2135 7.34766Z';
    @Output() selectedNavChange = new EventEmitter<string>();
    select(svgPath: string): void {
        this.selectedSvg = svgPath;
        switch (svgPath) {
            case this.homeSvg:
                this.selectedNavChange.emit('Home');
                this.router.navigate(['/home']);
                break;
            case this.otherSvg1:
                this.selectedNavChange.emit('Page 2');
                break;
            case this.otherSvg2:
                this.selectedNavChange.emit('Page 3');
                break;
        }
    }

    switchTheme(): void {
        this.themeService.switchTheme();
    }

    isDarkModeActive(): boolean {
        return this.themeService.isDarkModeActive();
    }
}
