import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DiscService } from '../../../core/services/disc';
import { LoanService } from '../../../core/services/loan';
import { MemberService } from '../../../core/services/member';
import { Cliente, ClienteCreate } from '../../../models/cliente';
import { Disc } from '../../../models/disc';
import { Renta } from '../../../models/renta';

@Component({
  imports: [FormsModule, RouterLink],
  selector: 'app-loan-form',
  styleUrl: './loan-form.scss',
  templateUrl: './loan-form.html',
})
export class LoanForm implements OnInit {
  disc = signal<Disc | null>(null);
  member = signal<Cliente | null>(null);
  loan = signal<Renta | null>(null);
  notMember = signal(false);
  loadingDisc = signal(true);
  lookupLoading = signal(false);
  submitting = signal(false);
  error = signal('');
  email = '';
  newMember: ClienteCreate = { nombre: '', email: '', telefono: '' };

  constructor(
    private route: ActivatedRoute,
    private discService: DiscService,
    private memberService: MemberService,
    private loanService: LoanService,
  ) {}

  ngOnInit() {
    const discId = this.route.snapshot.paramMap.get('discId');
    if (!discId) {
      this.error.set('No hay disco seleccionado. Por favor, regrese a la lista de discos y seleccione uno.');
      this.loadingDisc.set(false);
      return;
    }

    this.discService.get(discId).subscribe({
      next: (disc) => this.disc.set(disc),
      error: () => {
        this.error.set('No se pudo cargar el disco seleccionado.');
        this.loadingDisc.set(false);
      },
      complete: () => this.loadingDisc.set(false),
    });
  }

  formatearFechaDevolucion(date: string): string {
    return new Intl.DateTimeFormat('es', {
      dateStyle: 'long',
      timeZone: 'UTC',
    }).format(new Date(`${date}T00:00:00Z`));
  }

  marcarNoCliente() {
    this.notMember.set(true);
    this.member.set(null);
  }

  buscarCliente() {
    this.error.set('');
    this.member.set(null);
    this.notMember.set(false);
    this.lookupLoading.set(true);

    this.memberService.findByEmail(this.email.trim()).subscribe({
      next: (member) => this.member.set(member),
      error: (response) => {
        if (response.status === 404) {
          this.notMember.set(true);
        } else {
          this.error.set('No se pudo buscar este correo electrónico. Por favor, inténtelo de nuevo.');
        }
        this.lookupLoading.set(false);
      },
      complete: () => this.lookupLoading.set(false),
    });
  }

  cambiarEstadoCliente() {
    const member = this.member();
    if (!member) return;

    this.error.set('');
    this.memberService.setActive(member, member.estado !== 'activo').subscribe({
      next: (updated) => this.member.set(updated),
      error: () => this.error.set('No se pudo actualizar esta cuenta. Por favor, inténtelo de nuevo.'),
    });
  }

  registrarCliente() {
    this.error.set('');
    this.memberService.create({ ...this.newMember, email: this.newMember.email.trim() }).subscribe({
      next: (member) => {
        this.member.set(member);
        this.email = member.email;
        this.notMember.set(false);
      },
      error: (response) => this.error.set(response.status === 422
        ? 'Verifique que el nombre y el correo electrónico sean válidos.'
        : 'No se pudo crear esta cuenta. Por favor, inténtelo de nuevo.'),
    });
  }

  crearPrestamo() {
    const member = this.member();
    const disc = this.disc();
    if (!member || !disc || member.estado !== 'activo') return;

    this.error.set('');
    this.submitting.set(true);
    this.loanService.create({ cliente_id: member.id, disco_id: disc.id }).subscribe({
      next: (loan) => this.loan.set(loan),
      error: (response) => {
        this.error.set(response.status === 409
          ? 'No hay copias disponibles de este disco.'
          : 'No se pudo crear el préstamo. Confirme que la cuenta esté activa e inténtelo de nuevo.');
        this.submitting.set(false);
      },
      complete: () => this.submitting.set(false),
    });
  }
}
