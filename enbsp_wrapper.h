
#ifdef __cplusplus
extern "C" {
#endif

// Tipo de callback mais fácil (e só com o nescessário) para ser usada pelo Python
typedef void (*tipo_callback_facil)(tipo_info_que_eu_quero, tipo_outra_info_que_eu_quero, ... etc);

// "Callback tradutora" que vai ser chamada pela eNBSP. Simplesmente chama a callback Python passando as informações relevantes.
NBioAPI_RETURN callback_tradutora(NBioAPI_INDEXSEARCH_CALLBACK_PARAM_PTR_0 info, NBioAPI_VOID_PTR UserCallBackParam)
{
  tipo_callback_facil* callback_python_ptr = (tipo_callback_facil*) UserCallBackParam;
  
  // Chamando a callback Python
  callback_python_ptr(info->TotalCount, info->ProgressPos, ... etc);
  
  return /* alguma coisa */;
}

// Função de identificação usando a callback mais simples e destrinchando todas a structs para facilitar as coisas para o ctypes xD
bool WRAPPER_API identifica_mais_facil(
      // Handle (tipo primitivo, não precisa abrir)
      NBioAPI_HANDLE hHandle,
      
      // Abrindo struct NBioAPI_INPUT_FIR
      NBioAPI_INPUT_FIR_FORM Form,
      const NBioAPI_VOID_PTR FIR,
      
      // Nível de segurança (tipo primitivo, não precisa abrir)
      NBioAPI_FIR_SECURITY_LEVEL nSecuLevel,
      
      // Abrindo struct NBioAPI_INDEXSEARCH_FP_INFO
      NBioAPI_UINT32 ID,
      NBioAPI_UINT8  FingerID,
      NBioAPI_UINT8  SampleNumber,
      
      // Ponteiro para a callback mais simples usada no Python
      tipo_callback_facil callback_python_ptr)
{
  // Definição no header só pra exemplificar...
  
  // Dados do NBioAPI_INPUT_FIR_PTR
  NBioAPI_INPUT_FIR input_fir;
  input_fir.Form = Form;
  input_fir.FIR = FIR;
  
  // Dados do NBioAPI_INDEXSEARCH_FP_INFO_PTR
  NBioAPI_INDEXSEARCH_FP_INFO fp_info;
  fp_info.ID = ID;
  fp_info.FingerID = FingerID;
  fp_info.SampleNumber = SampleNumber;
  
  // Dados da callback, passando a "callback tradutora" e mais um ponteiro para a callback original
  NBioAPI_INDEXSEARCH_CALLBACK_INFO_0 callback_info;
  callback_info.CallBackType = /* não sei o que vai aqui */;
  callback_info.CallBackFunction = &callback_tradutora;
  callback_info.UserCallBackParam = (void*) callback_python_ptr;
  
  // Chama a função de identificação "verdadeira"
  NBioAPI_RETURN ret = NBioAPI_IdentifyDataFromIndexSearchDB(hHandle, &input_fir, nSecuLevel, &fp_info, &callback_info);
  
  return (ret == /* OK */);
}

// E é isso =)

#ifdef __cplusplus
}
#endif