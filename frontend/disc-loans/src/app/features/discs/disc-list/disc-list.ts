import { Component } from '@angular/core';
import { DiscService } from '../../../core/services/disc';
import { Disc } from '../../../models/disc';
import { Router } from '@angular/router';

@Component({
  imports: [],
  selector: 'app-disc-list',
  styleUrl: './disc-list.scss',
  templateUrl: './disc-list.html',
})
export class DiscList {
  discs: Disc[] = [];

  constructor(private discService: DiscService, public router: Router) {}
  ngOnInit(){
    this.discService.list().subscribe((discs: Disc[]) => {
      this.discs = discs;
    });
  }
}
