from pynetdicom3 import AE, VerificationPresentationContexts, PYNETDICOM_IMPLEMENTATION_UID, PYNETDICOM_IMPLEMENTATION_VERSION
from pynetdicom3.sop_class import CTImageStorage, MRImageStorage, StorageServiceClass
from pydicom.dataset import Dataset

ae = AE(ae_title=b'flavio-pacs', port=11112)
# Or we can use the inbuilt VerificationPresentationContexts list,
#   there's one for each of the supported Service Classes
# In this case, we are supporting any requests to use Verification SOP
#   Class in the association
ae.supported_contexts = VerificationPresentationContexts
#ae.add_supported_context(StorageServiceClass)
ae.add_supported_context(CTImageStorage)
ae.add_supported_context(MRImageStorage)

# Implement the AE.on_c_store callback
def on_c_store(ds, context, info):
    """Store the pydicom Dataset `ds`.

    Parameters
    ----------
    ds : pydicom.dataset.Dataset
        The dataset that the peer has requested be stored.
    context : namedtuple
        The presentation context that the dataset was sent under.
    info : dict
        Information about the association and storage request.

    Returns
    -------
    status : int or pydicom.dataset.Dataset
        The status returned to the peer AE in the C-STORE response. Must be
        a valid C-STORE status value for the applicable Service Class as
        either an ``int`` or a ``Dataset`` object containing (at a
        minimum) a (0000,0900) *Status* element.
    """
    # Add the DICOM File Meta Information
    meta = Dataset()
    meta.MediaStorageSOPClassUID = ds.SOPClassUID
    meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
    meta.ImplementationClassUID = PYNETDICOM_IMPLEMENTATION_UID
    meta.ImplementationVersionName = PYNETDICOM_IMPLEMENTATION_VERSION
    meta.TransferSyntaxUID = context.transfer_syntax

    # Add the file meta to the dataset
    ds.file_meta = meta

    # Set the transfer syntax attributes of the dataset
    ds.is_little_endian = context.transfer_syntax.is_little_endian
    ds.is_implicit_VR = context.transfer_syntax.is_implicit_VR

    # Save the dataset using the SOP Instance UID as the filename
    ds.save_as(ds.SOPInstanceUID, write_like_original=False)

    # Return a 'Success' status
    return 0x0000

ae.on_c_store = on_c_store

# Start the SCP
ae.start()