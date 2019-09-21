#ifndef DoubleToShortCaster_h
#define DoubleToShortCaster_h

#ifndef MESSAGE
#define MESSAGE cout << "file " << __FILE__ << " line " << __LINE__ << endl;
#endif
#ifndef ERR_MESSAGE
#define ERR_MESSAGE cout << "Error in file " << __FILE__ << " at line " << __LINE__  << " Exiting" <<  endl; exit(1);
#endif
#include <stdint.h>
#include "DataCaster.h"
#include "CasterRound.h"

using namespace std;

class DoubleToShortCaster : public DataCaster
{
    public:
        DoubleToShortCaster()
        {
            DataSizeIn = sizeof(double);
            DataSizeOut = sizeof(short);
            TCaster = (void *) new CasterRound<double,short>();
        }
        virtual ~DoubleToShortCaster()
        {
            delete (CasterRound<double,short> *) TCaster;
        }
        void convert(char * in,char * out, int numEl)
        {
            ((CasterRound<double,short> *) (TCaster))->convert(in, out, numEl);
        }

};
#endif //DoubleToShortCaster_h
