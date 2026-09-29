import { Component, signal } from '@angular/core';
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
  discs = signal<Disc[]>([]);

  constructor(private discService: DiscService, private router: Router) {}

  ngOnInit() {
    this.discService.list().subscribe((discs: Disc[]) => {
      this.discs.set(discs);
    });
  }

  seleccionarDisco(disc: Disc) {
    this.router.navigate(['/loans', disc.id]);
  }
}
