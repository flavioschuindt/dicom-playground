from pydicom import dcmread
from pydicom.uid import ImplicitVRLittleEndian

from pynetdicom3 import AE, VerificationPresentationContexts, StoragePresentationContexts
from pynetdicom3.sop_class import CTImageStorage, MRImageStorage

ae = AE(ae_title=b'MY_STORAGE_SCU')
# We can also do the same thing with the requested contexts
ae.requested_contexts = StoragePresentationContexts
# Or we can use inbuilt objects like CTImageStorage.
# The requested presentation context's transfer syntaxes can also
#   be specified using a str/UID or list of str/UIDs
#ae.add_requested_context(CTImageStorage,
                         #transfer_syntax=ImplicitVRLittleEndian)
# Adding a presentation context with multiple transfer syntaxes
#ae.add_requested_context(MRImageStorage,
                         #transfer_syntax=[ImplicitVRLittleEndian,
                                          #'1.2.840.10008.1.2.1'])

#ae.add_requested_context(VerificationPresentationContexts)

assoc = ae.associate('127.0.0.1', 11112)
if assoc.is_established:
    dataset = dcmread('test/dcm/CTImageStorage.dcm')
    # `status` is the response from the peer to the store request
    # but may be an empty pydicom Dataset if the peer timed out or
    # sent an invalid dataset.
    status = assoc.send_c_store(dataset)

    assoc.release()