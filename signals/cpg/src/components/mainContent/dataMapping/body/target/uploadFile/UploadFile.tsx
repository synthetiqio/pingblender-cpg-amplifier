import { Upload } from '@graffiti/react-components/upload';
import { Field } from '@graffiti/react-components/field';
import { useTargetUploadStore } from '@/stores/targetUpload';

import './uploadFile.scss';

type DataItem = {
    value:string; 
    label:string;
}

type PreviousMappingProps = {
    data: DataItem[];
}

function UploadFile({ data }: PreviousMappingProps) {
    const presetName = useTargetUploadStore((state) => state.preset);
    const setPresetName = useTargetUploadStore((state) => state.setPreset);
    const setTargetFile = useTargetUploadStore((state) => state.setTargetFile);
    const setIsFileUploaded= useTargetUploadStore(
        (state) => state.setIsFileUploaded
    );
    const setPresetTaken = useTargetUploadStore((state) => state.setPresetTaken);

    const onChangePresentName = (value: never) => {
        setPresetName(value);
    };

    const onChangeTargetUpload = (file:any): void => {
        setTargetFile(file);
    };

    const isPresetNameTaken = () => {
        const labels = data.map((presetObj) => presetObj.label);
        const presetTaken = labels.includes(presetName);
        setPresetTaken(presetTaken);
        return presetTaken; 
    };

    return (
        <div>
            <div className='ap-field-demo-wrapper'>
                <Input 
                  type="text"
                  title="Preset Name"
                  required
                  value={presetName}
                  onChange={onChangePresetName}
                  error={isPresetNameTaken()}
                  errorNode={
                    <div 
                       id="errormessage"
                       aria-live="polite"
                       className="ap-field-email-validation-error"
                       >
                        Preset name already taken. Please choose another label.
                    </div>
                  }
            />
        </div>
        <Upload 
          className="upload-form"
          onSuccess={()=> setIsFileUploaded(true)}
          onRemove={()=> setIsFileUploaded(false)}
          onChange={onChangeTargetUpload}
          multiple={false}
          autoUpload
          acceptFileType=".csv"
          uploadInstruction="Only single files in CSV format are accepted"
          uploadTitle="Upload your custom target file"
          maxFileSize={10 * 1024 * 1024}
          config={{
            trigger:false,
            type:'inline', 
            size:true 
          }}
       />
    );
}
