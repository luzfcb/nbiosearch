#include <string.h>
#include <Python.h>
#include <NBioAPI.h>
#include <NBioAPI_IndexSearch.h>


static PyObject *bsp_open(PyObject *self, PyObject *args)
{
    NBioAPI_RETURN err;
    NBioAPI_HANDLE m_hBSP;
    NBioAPI_VERSION m_Version;

    err = NBioAPI_Init(&m_hBSP);
    if(err != NBioAPIERROR_NONE)
        return PyErr_Format(PyExc_RuntimeError, "cannot initialize Nitgen API");

    NBioAPI_GetVersion(m_hBSP, &m_Version);


    return Py_BuildValue("(iii)", m_hBSP, m_Version.Major, m_Version.Minor);
}

static PyObject *bsp_close(PyObject *self, PyObject *args)
{
    NBioAPI_HANDLE m_hBSP;
    //NBioAPI_RETURN ret;
    if(!PyArg_ParseTuple(args, "i", &m_hBSP))
        return PyErr_Format(PyExc_TypeError, "invalid bsp handler");

    NBioAPI_Terminate(m_hBSP);
    //ret = NBioAPI_Terminate(m_hBSP);

    Py_INCREF(Py_None);
    return Py_None;
}


static PyObject *search_initialize(PyObject *self, PyObject *args)
{
    NBioAPI_RETURN err;
    NBioAPI_HANDLE m_hBSP;

    if(!PyArg_ParseTuple(args, "i", &m_hBSP))
        return PyErr_Format(PyExc_TypeError, "invalid bsp handler");

    err = NBioAPI_InitIndexSearchEngine(m_hBSP);
    if(err != NBioAPIERROR_NONE)
        return PyErr_Format(PyExc_RuntimeError, "cannot initialize search engine");

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *search_terminate(PyObject *self, PyObject *args)
{
    NBioAPI_RETURN err;
    NBioAPI_HANDLE m_hBSP;

    if(!PyArg_ParseTuple(args, "i", &m_hBSP))
        return PyErr_Format(PyExc_TypeError, "invalid bsp handler");

    err = NBioAPI_TerminateIndexSearchEngine(m_hBSP);
    if(err != NBioAPIERROR_NONE)
        return PyErr_Format(PyExc_RuntimeError, "cannot terminate search engine");

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *search_insert(PyObject *self, PyObject *args)
{
    PyObject *rawFIR;
    NBioAPI_RETURN err;
    NBioAPI_HANDLE m_hBSP;
    NBioAPI_UINT32 userID;
    NBioAPI_INPUT_FIR inputFIR;
    NBioAPI_FIR_HANDLE fir_handle;
    NBioAPI_FIR_TEXTENCODE fir_text;
    NBioAPI_INDEXSEARCH_SAMPLE_INFO sample;

    if(!PyArg_ParseTuple(args, "iiO", &m_hBSP, &userID, &rawFIR))
        return PyErr_Format(PyExc_TypeError, "invalid arguments");

    /* determine format of FIR: handler or text */
    if(PyInt_Check(rawFIR)) {
        PyArg_Parse(rawFIR, "i", &fir_handle);
        inputFIR.Form = NBioAPI_FIR_FORM_HANDLE;
        inputFIR.InputFIR.FIRinBSP = &fir_handle;
    } else if(PyString_Check(rawFIR)) {
        PyArg_Parse(rawFIR, "s", &fir_text.TextFIR);
        fir_text.IsWideChar = NBioAPI_FALSE;
        inputFIR.Form = NBioAPI_FIR_FORM_TEXTENCODE;
        inputFIR.InputFIR.TextFIR = &fir_text;
    } else
        return PyErr_Format(PyExc_TypeError, "unknown format of FIR");

    memset(&sample, 0, sizeof(sample));
    err = NBioAPI_AddFIRToIndexSearchDB(m_hBSP, &inputFIR, userID, &sample);
    if(err != NBioAPIERROR_NONE)
        return PyErr_Format(PyExc_RuntimeError, "cannot add FIR to search engine");

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *search_remove(PyObject *self, PyObject *args)
{
    NBioAPI_RETURN err;
    NBioAPI_HANDLE m_hBSP;
    NBioAPI_UINT32 userID;

    if(!PyArg_ParseTuple(args, "ii", &m_hBSP, &userID))
        return PyErr_Format(PyExc_TypeError, "invalid arguments");

    err = NBioAPI_RemoveUserFromIndexSearchDB(m_hBSP, userID);
    if(err != NBioAPIERROR_NONE)
        return PyErr_Format(PyExc_RuntimeError, "cannot remove FIR from search engine");

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *search_identify(PyObject *self, PyObject *args)
{
    int seclevel;
    PyObject *rawFIR;
    NBioAPI_RETURN err;
    NBioAPI_HANDLE m_hBSP;
    NBioAPI_INPUT_FIR inputFIR;
    NBioAPI_FIR_HANDLE fir_handle;
    NBioAPI_FIR_TEXTENCODE fir_text;
    NBioAPI_INDEXSEARCH_FP_INFO info;

    if(!PyArg_ParseTuple(args, "iOi", &m_hBSP, &rawFIR, &seclevel))
        return PyErr_Format(PyExc_TypeError, "invalid arguments");

    /* determine format of FIR: handler or text */
    if(PyInt_Check(rawFIR)) {
        PyArg_Parse(rawFIR, "i", &fir_handle);
        inputFIR.Form = NBioAPI_FIR_FORM_HANDLE;
        inputFIR.InputFIR.FIRinBSP = &fir_handle;
    } else if(PyString_Check(rawFIR)) {
        PyArg_Parse(rawFIR, "s", &fir_text.TextFIR);
        fir_text.IsWideChar = NBioAPI_FALSE;
        inputFIR.Form = NBioAPI_FIR_FORM_TEXTENCODE;
        inputFIR.InputFIR.TextFIR = &fir_text;
    } else
        return PyErr_Format(PyExc_TypeError, "unknown format of FIR");

    memset(&info, 0, sizeof(info));
    err = NBioAPI_IdentifyDataFromIndexSearchDB(m_hBSP, &inputFIR, seclevel, &info, NULL);
    if(err == NBioAPIERROR_INDEXSEARCH_IDENTIFY_FAIL) {
        Py_INCREF(Py_None);
        return Py_None;
    }

    if(err == NBioAPIERROR_INVALID_HANDLE){
        return PyErr_Format(PyExc_RuntimeError, "Invalid NBioAPI handle.");
    }
    if(err == NBioAPIERROR_INVALID_POINTER){
        return PyErr_Format(PyExc_RuntimeError, "Invalid parameter pointer.");
    }
    if(err == NBioAPIERROR_INDEXSEARCH_INIT_FAIL){
        return PyErr_Format(PyExc_RuntimeError, "IndexSearch engine not initialized.");
    }
    if(err == NBioAPIERROR_INDEXSEARCH_IDENTIFY_STOP){
        return PyErr_Format(PyExc_RuntimeError, "Identification stopped by callback functions.");
    }
    if(err == NBioAPIERROR_UNKNOWN_INPUTFORMAT){
        return PyErr_Format(PyExc_RuntimeError, "Known input format.");
    }
    if(err == NBioAPIERROR_UNKNOWN_FORMAT){
        return PyErr_Format(PyExc_RuntimeError, "Known format.");
    }


    if(err != NBioAPIERROR_NONE){
        return PyErr_Format(PyExc_RuntimeError, "cannot perform identify within the search engine");
    }


    return Py_BuildValue("i", info.ID);
}

static PyObject *search_save(PyObject *self, PyObject *args)
{
    NBioAPI_RETURN err;
    NBioAPI_HANDLE m_hBSP;
    NBioAPI_CHAR *fullpath;

    if(!PyArg_ParseTuple(args, "is", &m_hBSP, &fullpath))
        return PyErr_Format(PyExc_TypeError, "invalid arguments");

    err = NBioAPI_SaveIndexSearchDBToFile(m_hBSP, fullpath);
    if(err != NBioAPIERROR_NONE)
        return PyErr_Format(PyExc_RuntimeError, "cannot save search engine DB to file");

    Py_INCREF(Py_None);
    return Py_True;
    //return Py_None;
}

static PyObject *search_load(PyObject *self, PyObject *args)
{
    NBioAPI_RETURN err;
    NBioAPI_HANDLE m_hBSP;
    NBioAPI_CHAR *fullpath;

    if(!PyArg_ParseTuple(args, "is", &m_hBSP, &fullpath))
        return PyErr_Format(PyExc_TypeError, "invalid arguments");

    err = NBioAPI_LoadIndexSearchDBFromFile(m_hBSP, fullpath);
    if(err != NBioAPIERROR_NONE)
        return PyErr_Format(PyExc_RuntimeError, "cannot load search engine DB from file");

    Py_INCREF(Py_None);
    return Py_True;
    //return Py_None;
}

static PyObject *bsp_verify(PyObject *self, PyObject *args)
{
    NBioAPI_RETURN err;
    NBioAPI_HANDLE m_hBSP;
    NBioAPI_FIR_PAYLOAD payload;
    NBioAPI_INPUT_FIR cap1, cap2;
    NBioAPI_BOOL bResult = NBioAPI_FALSE;
    NBioAPI_FIR_HANDLE fir1_handle, fir2_handle;
    NBioAPI_FIR_TEXTENCODE fir1_text, fir2_text;
    PyObject *rawF1, *rawF2;

    if(!PyArg_ParseTuple(args, "iOO", &m_hBSP, &rawF1, &rawF2))
        return PyErr_Format(PyExc_TypeError, "invalid arguments");

    /* determine format of FIR 1: handler or text */
    if(PyInt_Check(rawF1)) {
        PyArg_Parse(rawF1, "i", &fir1_handle);
        cap1.Form = NBioAPI_FIR_FORM_HANDLE;
        cap1.InputFIR.FIRinBSP = &fir1_handle;
    } else if(PyString_Check(rawF1)) {
        PyArg_Parse(rawF1, "s", &fir1_text.TextFIR);
        fir1_text.IsWideChar = NBioAPI_FALSE;
        cap1.Form = NBioAPI_FIR_FORM_TEXTENCODE;
        cap1.InputFIR.TextFIR = &fir1_text;
    } else
        return PyErr_Format(PyExc_TypeError, "unknown format of cap1");

    /* determine format of FIR 2: handler or text */
    if(PyInt_Check(rawF2)) {
        PyArg_Parse(rawF2, "i", &fir2_handle);
        cap2.Form = NBioAPI_FIR_FORM_HANDLE;
        cap2.InputFIR.FIRinBSP = &fir2_handle;
    } else if(PyString_Check(rawF2)) {
        PyArg_Parse(rawF2, "s", &fir2_text.TextFIR);
        fir2_text.IsWideChar = NBioAPI_FALSE;
        cap2.Form = NBioAPI_FIR_FORM_TEXTENCODE;
        cap2.InputFIR.TextFIR = &fir2_text;
    } else
        return PyErr_Format(PyExc_TypeError, "unknown format of cap2");

    /* warning: cannot verify text VS handle and vice-versa */
    memset(&payload, 0, sizeof(payload));
    err = NBioAPI_VerifyMatch(m_hBSP, &cap1, &cap2, &bResult, &payload);
    if(err != NBioAPIERROR_NONE)
        switch(err) {
            case NBioAPIERROR_INVALID_HANDLE:
                return PyErr_Format(PyExc_RuntimeError, "cannot verify: invalid handle");
            case NBioAPIERROR_INVALID_POINTER:
                return PyErr_Format(PyExc_RuntimeError, "cannot verify: invalid pointer");
            case NBioAPIERROR_ENCRYPTED_DATA_ERROR:
                return PyErr_Format(PyExc_RuntimeError, "cannot verify: encrypted data error");
            case NBioAPIERROR_INTERNAL_CHECKSUM_FAIL:
                return PyErr_Format(PyExc_RuntimeError, "cannot verify: checksum fail");
            case NBioAPIERROR_MUST_BE_PROCESSED_DATA:
                return PyErr_Format(PyExc_RuntimeError, "cannot verify: must be processed data");
            default:
                return PyErr_Format(PyExc_RuntimeError, "cannot verify: unknown reason");
        }
    return Py_BuildValue("is#", bResult, payload.Data, payload.Length);
}

static PyObject *bsp_free_fir(PyObject *self, PyObject *args)
{
    NBioAPI_HANDLE m_hBSP;
    NBioAPI_FIR_HANDLE fir;

    if(!PyArg_ParseTuple(args, "ii", &m_hBSP, &fir))
        return PyErr_Format(PyExc_TypeError, "invalid arguments");

    NBioAPI_FreeFIRHandle(m_hBSP, fir);
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *bsp_text_fir(PyObject *self, PyObject *args)
{
    NBioAPI_RETURN err;
    NBioAPI_HANDLE m_hBSP;
    NBioAPI_FIR_HANDLE fir;
    NBioAPI_FIR_TEXTENCODE TextFIR;

    if(!PyArg_ParseTuple(args, "ii", &m_hBSP, &fir))
        return PyErr_Format(PyExc_TypeError, "invalid arguments");

    err = NBioAPI_GetTextFIRFromHandle(m_hBSP, fir, &TextFIR, NBioAPI_FALSE);
    if(err != NBioAPIERROR_NONE)
        return PyErr_Format(PyExc_RuntimeError, "cannot retrieve text-encoded FIR");

    return Py_BuildValue("s", TextFIR.TextFIR);
}

static PyObject *bsp_payload(PyObject *self, PyObject *args)
{
    NBioAPI_RETURN err;
    NBioAPI_HANDLE m_hBSP;
    NBioAPI_INPUT_FIR inputFIR;
    NBioAPI_FIR_PAYLOAD payload;
    NBioAPI_FIR_HANDLE fir_handle, fir_template;

    memset(&payload, 0, sizeof(payload));
    if(!PyArg_ParseTuple(args, "iis#", &m_hBSP, &fir_handle, &payload.Data, &payload.Length))
        return PyErr_Format(PyExc_TypeError, "invalid arguments");

    memset(&inputFIR, 0, sizeof(inputFIR));
    inputFIR.Form = NBioAPI_FIR_FORM_HANDLE;
    inputFIR.InputFIR.FIRinBSP = &fir_handle;

    err = NBioAPI_CreateTemplate(m_hBSP, &inputFIR, NULL, &fir_template, &payload);
    if(err != NBioAPIERROR_NONE)
        return PyErr_Format(PyExc_RuntimeError, "cannot create template from FIR handle");

    NBioAPI_FreeFIRHandle(m_hBSP, fir_handle);
    return Py_BuildValue("i", fir_template);
}



static PyMethodDef SearchMethods[] = {
    {"initialize", search_initialize, METH_VARARGS, "initialize search engine"},
    {"terminate", search_terminate, METH_VARARGS, "terminate search engine"},
    {"insert", search_insert, METH_VARARGS, "insert userID with FIR into the search engine"},
    {"remove", search_remove, METH_VARARGS, "remove userID from the search engine"},
    {"identify", search_identify, METH_VARARGS, "identify FIR using search engine"},
    {"save", search_save, METH_VARARGS, "save search engine db into file"},
    {"load", search_load, METH_VARARGS, "load search engine db from file"},
    // extracted from bsp_core.c
    {"open", bsp_open, 0, "open bsp API"},
    {"close", bsp_close, METH_VARARGS, "close bsp API"},
    {"verify", bsp_verify, METH_VARARGS, "verify fingerprints"},
    {"free_fir", bsp_free_fir, METH_VARARGS, "release FIR memory"},
    {"text_fir", bsp_text_fir, METH_VARARGS, "return text-encoded FIR"},
    {"payload", bsp_payload, METH_VARARGS, "set FIR payload"},

    {NULL, NULL, 0, NULL},
};

PyMODINIT_FUNC init_bsp_search(void)
{
    Py_InitModule("_bsp_search", SearchMethods);
}
