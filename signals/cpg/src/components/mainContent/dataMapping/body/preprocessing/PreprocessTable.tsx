import { Table, Column } from '@graffiti/react-components/table';
import { useState, useEffect } from 'react';
import { Badge } from '@graffiti/react-components/badge'; 
import { Input } from '@graffiti/react-components/field';
import { Select } from '@graffiti/reac-components/select';

import './preprocessing.scss'; 
import './preprocessingNoDataMessage.scss'
import { PreprocessingNoDataMessage } from './PreprocessingNoDataMessage';
import { PreprocessingConfidence } from '@/utils/enums';
import { usePreprocessingStore } from '@/stores/preprocessing';

function PreprocessTable(){
    const preProcessData = usePreprocessingStore (
        (state: any) => state.preprocessingData
    );

    const setPreprocessingData = usePreprocessingStore(
        (state:any) => state.usePreprocessingData
    
    ); 

    const [tdata, setTdata] = useState([]);
    //const [loading, setLoading] = useState(true);
     
    const updateFormatValue = usePreprocessingStore(
        (state:any) => state.updateFormatValue
    );

    const updateColumnHeader = usePreprocessingStore(
        (state:any) => state.updateColumnHeader
    );

    const updateChangeTracker = usePreprocessingStore(
        (state:any) => state.updateChangeTracker
    );

    const filterAIGenerated = (data:any) => {
        const filteredAIData = data.filter((obj:any) => obj.ai_generated === true);
        return filteredAIData
    }; 

    //data loading.
    useEffect(()=> {
        if(preProcessData && preProcessData.length > 0){
            const aiDataOnly = filterAIGenerated(preProcessData);
            setPreprocessingData(aiDataOnly); 
            setTdata(aiDataOnly);
        }

    }, []);

    const handleHeaderChange = (id: string, newHeader: string) => {
        updateColumnHeader(id, newHeader); 
        //updateColumnHeader(id, newHeader);
        updateChangeTracker(id, {assigned_header: newHeader});
    };

    const handleFormatChange = (id: string, newFormat:any) => {
        updateFormatValue(id, {value: newFormat, label: newFormat});
        updateChangeTracker(id, {format: { value: newFormat, label: newFormat }});
    };

    const renderConfidenceBadge = (row:any, field:string) => {
        let badgeColor = '';
        if (row[field] === PreprocessingConfidence.High){
            badgeColor = 'success-outlined'; 
        } else if (row[field] === PreprocessingConfidence.Medium){
            badgeColor = 'warning-outlined'; 
        } else if (row[field] === PreprocessingConfidence.Low){
            badgeColor = 'danger-outlined';
        } else {
            badgeColor = 'info-outlined';
        }

      return (
        <Badge
          className="confidence-badge"
          value={`${row[field]}`}
          type={badgeColor}
         />
      );
    };

    const renderColumnHeader = (row:any, field:string) => {
        return (
            <div className="ap-field-demo-wrapper">
                <Input 
                    hideTitleOnInput
                    placeholder="column header"
                    type="text"
                    title="Column header"
                    defaultValue={row[field]}
                    onBlur={(e:any) => handleHeaderChange(row.id, e.target.value)}
                />
            </div>
            );
    };

    const possibilities = [
        { value:'Currency', label:'Currency'},
        { value:'Date', label:'Date'}, 
        { value:'General', label:'General'}, 
        { value:'Number', label: 'Number'}, 
        { value:'Percentage', label:'Percentage'},
        { value:'Text', label:'Text'},
    ];


    const renderFormat = (row:any)=> {
       return (
         <Select 
            hideTitleOnInput
            dropdownAlwaysDown={false}
            data={possibilities}
            defaultValue={row?.format?.value}
            onSelect={(value)=> handleFormatChange(row.id, value)}
         />
        );
    };

    return tdata?.length > 0 ? (
        <div className="preprocessTable">
            <Table 
              originalData={tdata}
              hasTitle
              striped
              condensed
              skipInitialSort
              tableId="preprocess"
            >
                <Column field="confidence" renderCell={renderConfidenceBadge}>
                  Confidence
                </Column>
                <Column field="suggested_header" renderCell={renderColumnHeader}>
                  Column Header
                </Column>
                <Column field="format" renderCell={renderFormat}>
                  Format
                </Column>
                <Column field="sample 1">Sample 1</Column>
                <Column field="sample 2">Sample 2</Column>
                <Column field="sample 3">Sample 3</Column>
                <Column field="sample 4">Sample 4</Column>
            </Table>
         </div>
    ) : (
        <PreprocessingNoDataMessage />
    );
}

export { PreprocessTable }