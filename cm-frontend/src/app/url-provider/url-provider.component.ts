import { Component, ViewChild } from '@angular/core';
import { OptionsComponent } from '../options/options.component';
import { CommonModule } from '@angular/common';
import { ApiService } from '../_services/api.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-url-provider',
  standalone: true,
  imports: [OptionsComponent, CommonModule, FormsModule],
  templateUrl: './url-provider.component.html',
  styleUrl: './url-provider.component.scss'
})
export class UrlProviderComponent {
  
  constructor(private api: ApiService) {}

  @ViewChild(OptionsComponent) optionsForm!:OptionsComponent;
  
  status: "initial" | "waiting" | "processing" | "success" | "fail" = "initial"; 
  url: string | null = null;

  onChange() {
    console.log("test")
    if (this.url === "") {
      this.status = "initial";
    } else {
      this.status = "waiting";
    }
  }

  onUpload() {
    if (this.url) {
      this.status = "processing";

      let options = this.optionsForm.getOptions()

      this.api.postURL(this.url, options).subscribe({
        next: res => this.status = 'success',
        error: err => this.status = 'fail'
      });
    }
  }

  onClear() {
    if (this.status == 'processing') {
      return;
    }
    
    this.status = 'initial'
    this.url = null;
    this.optionsForm.resetOptions();
  }
}
