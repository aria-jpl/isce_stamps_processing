#ifndef LongToShortCpxCaster_h
#define LongToShortCpxCaster_h

#ifndef MESSAGE
#define MESSAGE cout << "file " << __FILE__ << " line " << __LINE__ << endl;
#endif
#ifndef ERR_MESSAGE
#define ERR_MESSAGE cout << "Error in file " << __FILE__ << " at line " << __LINE__  << " Exiting" <<  endl; exit(1);
#endif
#include <complex>
#include <stdint.h>
#include "DataCaster.h"
#include "Caster.h"

using namespace std;

class LongToShortCpxCaster : public DataCaster
{
    public:
        LongToShortCpxCaster()
        {
            DataSizeIn = sizeof(complex<long>);
            DataSizeOut = sizeof(complex<short>);
            TCaster = (void *) new Caster<complex<long>,complex<short> >();
        }
        virtual ~LongToShortCpxCaster()
        {
            delete (Caster<complex<long>,complex<short> > *) TCaster;
        }
        void convert(char * in,char * out, int numEl)
        {
            ((Caster<complex<long>,complex<short> > *) (TCaster))->convert(in, out, numEl);
        }

};
#endif //LongToShortCpxCaster_h
