import { Component, ViewChild } from '@angular/core';
import { OptionsComponent } from '../options/options.component';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../_services/api.service';

@Component({
  selector: 'app-text-uploader',
  standalone: true,
  imports: [OptionsComponent, CommonModule, FormsModule],
  templateUrl: './text-uploader.component.html',
  styleUrl: './text-uploader.component.scss'
})
export class TextUploaderComponent {

  constructor(private api: ApiService) {}

  @ViewChild(OptionsComponent) optionsForm!:OptionsComponent;

  status: "initial" | "waiting" | "processing" | "success" | "fail" = "initial"; 
  text: string = "";

  onChange() {
    if (this.text === "") {
      this.status = "initial";
    } else {
      this.status = "waiting";
    }
  }

  onUpload() {
    if (this.text) {
      this.status = "processing";

      let options = this.optionsForm.getOptions()

      this.api.postText(this.text, options).subscribe({
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
    this.text = "";
    this.optionsForm.resetOptions();
  }

}
