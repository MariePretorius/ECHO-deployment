import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ThemeService } from './../../services/theme.service';
import { MoodService } from '../../services/mood-service.service';

@Component({
    selector: 'app-svg-icon',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './svg-icon.component.html',
    styleUrls: ['./svg-icon.component.css'],
})
export class SvgIconComponent {
      //Mood Service Variables
      moodComponentClasses!:{ [key: string]: string };
    
    @Input() svgPath?: string;
    @Input() fillColor?: string;
    @Input() selected?: boolean;
    @Output() svgClick = new EventEmitter<void>();
    constructor(private themeService: ThemeService, public moodService: MoodService) {}

    ngOnInit() {
        this.moodComponentClasses = this.moodService.getComponentMoodClasses(); 
    }
    onClick() {
        this.svgClick.emit();
    }

    circleColor(): string {
        return this.themeService.isDarkModeActive()
            ? this.moodComponentClasses[this.moodService.getCurrentMood()]
            : 'rgba(238, 2, 88, 0.5)';
    }
}
