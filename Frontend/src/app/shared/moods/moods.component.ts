import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { NgClass, NgForOf, NgIf } from '@angular/common';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatDialog } from '@angular/material/dialog';
import { SongViewComponent } from '../song-view/song-view.component';
import { ScreenSizeService } from '../../services/screen-size-service.service';

@Component({
    selector: 'app-moods',
    standalone: true,
    imports: [MatGridListModule, MatCardModule, NgClass, NgForOf, NgIf],
    templateUrl: './moods.component.html',
    styleUrl: './moods.component.css',
})
export class MoodsComponent {
    screenSize?: string;
    constructor(
        private screenSizeService: ScreenSizeService,
        protected dialog: MatDialog
    ) {}
    
    async ngOnInit() {
        this.screenSizeService.screenSize$.subscribe(screenSize => {
        this.screenSize = screenSize;
        });
    }
    favouriteMoods = [
        {
            name: 'Anxious',
            image: '/assets/moods/arctic.jpeg',
        },
        {
            name: 'Chill',
            image: '/assets/moods/kendrick.jpeg',
        },
        {
            name: 'Happy',
            image: '/assets/moods/gambino.jpeg',
        },
        {
            name: 'Melancholy',
            image: '/assets/moods/radiohead.jpeg',
        },
        {
            name: 'Nostalgic',
            image: '/assets/moods/sza.jpeg',
        },
        {
            name: 'Unknown',
            image: '/assets/moods/img6.jpg',
        },
    ];

    RecommendedMoods = [
        {
            name: 'Mad',
            image: '/assets/moods/yonce.jpeg',
        },
        {
            name: 'Nostalgic',
            image: '/assets/moods/taylor.jpeg',
        },
        {
            name: 'Ethereal',
            image: '/assets/moods/impala.jpeg',
        },
        {
            name: 'Confident',
            image: '/assets/moods/tyler.jpeg',
        },
        {
            name: 'Happy',
            image: '/assets/moods/beatles.jpeg',
        },
        {
            name: 'Introspective',
            image: '/assets/moods/happy.jpg',
        },
    ];

    selectedMood: any = null;

    openModal(mood: any): void {
        const dialogRef = this.dialog.open(SongViewComponent, {
            width: '250px',
        });

        dialogRef.afterClosed().subscribe((result) => {
            console.log('The dialog was closed');
        });
    }
}
