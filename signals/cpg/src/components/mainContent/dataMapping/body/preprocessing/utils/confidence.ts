export const sortFunctionForOrder1 = (a: any, b: any) => {
    const firstOrderId = a.confidenceIndex; 
    const secondOrderId = b.confidenceIndex; 
    return firstOrderId > secondOrderId ? 1: -1;
};

export const sortFuncForOrder2 = (a: any, b: any) => {
    const firstOrderId = a.confidenceIndex; 
    const secondOrderId = b.confidenceIndex; 
    return firstOrderId > secondOrderId ? -1 : 1;
}